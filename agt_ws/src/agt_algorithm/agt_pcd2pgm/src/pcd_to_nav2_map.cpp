// Adapted from the Apache-2.0 licensed upstream project:
// https://github.com/kzm784/pcd2pgm

#include "agt_pcd2pgm/pcd_to_nav2_map.hpp"

#include <pcl/PCLPointCloud2.h>
#include <pcl/conversions.h>
#include <pcl/filters/extract_indices.h>
#include <pcl/filters/statistical_outlier_removal.h>
#include <pcl/filters/voxel_grid.h>
#include <pcl/io/pcd_io.h>
#include <pcl/point_cloud.h>
#include <pcl/point_types.h>
#include <pcl/search/kdtree.h>
#include <pcl/segmentation/progressive_morphological_filter.h>

#include <algorithm>
#include <cmath>
#include <cstdint>
#include <filesystem>
#include <fstream>
#include <limits>
#include <sstream>
#include <vector>

namespace agt_pcd2pgm
{

namespace
{

bool load_pcd_as_xyz(
  const std::string & pcd_path,
  pcl::PointCloud<pcl::PointXYZ>::Ptr & cloud,
  std::string & error_message)
{
  pcl::PCLPointCloud2 raw_cloud;
  if (pcl::io::loadPCDFile(pcd_path, raw_cloud) != 0) {
    error_message = "Failed to read PCD file: " + pcd_path;
    return false;
  }

  pcl::fromPCLPointCloud2(raw_cloud, *cloud);
  if (cloud->empty()) {
    error_message = "PCD file is empty after conversion: " + pcd_path;
    return false;
  }

  return true;
}

bool resolve_output_paths(
  const ConversionOptions & input_options,
  ConversionOptions & resolved_options,
  std::filesystem::path & output_dir,
  std::string & error_message)
{
  resolved_options = input_options;
  if (resolved_options.pcd_path.empty()) {
    error_message = "pcd_path is empty.";
    return false;
  }

  const std::filesystem::path pcd_path(resolved_options.pcd_path);
  if (!std::filesystem::exists(pcd_path)) {
    error_message = "PCD file does not exist: " + resolved_options.pcd_path;
    return false;
  }

  output_dir = resolved_options.output_dir.empty() ? pcd_path.parent_path() : std::filesystem::path(resolved_options.output_dir);
  if (output_dir.empty()) {
    output_dir = ".";
  }

  if (resolved_options.save_map_name.empty()) {
    resolved_options.save_map_name = pcd_path.stem().string();
  }

  std::error_code ec;
  std::filesystem::create_directories(output_dir, ec);
  if (ec) {
    error_message = "Failed to create output directory: " + output_dir.string() + ", " + ec.message();
    return false;
  }

  return true;
}

bool save_debug_clouds(
  const std::filesystem::path & output_dir,
  const pcl::PointCloud<pcl::PointXYZ>::ConstPtr & cloud_downsample,
  const pcl::PointCloud<pcl::PointXYZ>::ConstPtr & cloud_ground,
  const pcl::PointCloud<pcl::PointXYZ>::ConstPtr & cloud_nonground,
  const pcl::PointCloud<pcl::PointXYZ>::ConstPtr & cloud_obstacles,
  std::string & error_message)
{
  if (pcl::io::savePCDFileBinary((output_dir / "cloud_downsample.pcd").string(), *cloud_downsample) != 0 ||
      pcl::io::savePCDFileBinary((output_dir / "cloud_ground.pcd").string(), *cloud_ground) != 0 ||
      pcl::io::savePCDFileBinary((output_dir / "cloud_nonground.pcd").string(), *cloud_nonground) != 0 ||
      pcl::io::savePCDFileBinary((output_dir / "cloud_obstacles.pcd").string(), *cloud_obstacles) != 0) {
    error_message = "Failed to save one or more debug PCD files.";
    return false;
  }

  return true;
}

bool save_pgm_and_yaml(
  const std::filesystem::path & output_dir,
  const ConversionOptions & options,
  const pcl::PointCloud<pcl::PointXYZ>::ConstPtr & cloud_obstacles,
  ConversionResult & result)
{
  if (!cloud_obstacles || cloud_obstacles->empty()) {
    result.message = "No obstacle points available after filtering.";
    return false;
  }

  double min_x = std::numeric_limits<double>::infinity();
  double min_y = std::numeric_limits<double>::infinity();
  double max_x = -std::numeric_limits<double>::infinity();
  double max_y = -std::numeric_limits<double>::infinity();

  for (const auto & point : cloud_obstacles->points) {
    min_x = std::min(min_x, static_cast<double>(point.x));
    min_y = std::min(min_y, static_cast<double>(point.y));
    max_x = std::max(max_x, static_cast<double>(point.x));
    max_y = std::max(max_y, static_cast<double>(point.y));
  }

  if (!std::isfinite(min_x) || !std::isfinite(min_y) ||
      !std::isfinite(max_x) || !std::isfinite(max_y)) {
    result.message = "Obstacle bounding box is invalid.";
    return false;
  }

  const int width = std::max(1, static_cast<int>(std::ceil((max_x - min_x) / options.resolution)));
  const int height = std::max(1, static_cast<int>(std::ceil((max_y - min_y) / options.resolution)));
  std::vector<uint16_t> counters(static_cast<std::size_t>(width) * static_cast<std::size_t>(height), 0);

  auto xy_to_index = [&](double x, double y) -> int {
    const int ix = static_cast<int>(std::floor((x - min_x) / options.resolution));
    const int iy = static_cast<int>(std::floor((y - min_y) / options.resolution));
    if (ix < 0 || ix >= width || iy < 0 || iy >= height) {
      return -1;
    }
    return iy * width + ix;
  };

  for (const auto & point : cloud_obstacles->points) {
    const int index = xy_to_index(point.x, point.y);
    if (index >= 0) {
      counters[static_cast<std::size_t>(index)] += 1;
    }
  }

  result.pgm_path = (output_dir / (options.save_map_name + ".pgm")).string();
  std::ofstream pgm_stream(result.pgm_path, std::ios::binary);
  if (!pgm_stream) {
    result.message = "Failed to open output PGM: " + result.pgm_path;
    return false;
  }

  pgm_stream << "P5\n" << width << " " << height << "\n255\n";
  for (int y = height - 1; y >= 0; --y) {
    for (int x = 0; x < width; ++x) {
      const int index = y * width + x;
      uint8_t pixel = 254;
      if (counters[static_cast<std::size_t>(index)] >= static_cast<uint16_t>(options.min_points_per_cell)) {
        pixel = 0;
      }
      pgm_stream.write(reinterpret_cast<char *>(&pixel), 1);
    }
  }
  pgm_stream.close();

  result.yaml_path = (output_dir / (options.save_map_name + ".yaml")).string();
  std::ofstream yaml_stream(result.yaml_path);
  if (!yaml_stream) {
    result.message = "Failed to open output YAML: " + result.yaml_path;
    return false;
  }

  yaml_stream << "image: " << options.save_map_name + ".pgm" << "\n";
  yaml_stream << "mode: trinary\n";
  yaml_stream << "resolution: " << options.resolution << "\n";
  yaml_stream << "origin: [" << min_x << ", " << min_y << ", 0.0]\n";
  yaml_stream << "negate: 0\n";
  yaml_stream << "occupied_thresh: 0.65\n";
  yaml_stream << "free_thresh: 0.196\n";
  yaml_stream.close();

  result.width = width;
  result.height = height;
  return true;
}

}  // namespace

bool convert_pcd_to_nav2_map(const ConversionOptions & options, ConversionResult & result)
{
  ConversionOptions resolved_options;
  std::filesystem::path output_dir;
  if (!resolve_output_paths(options, resolved_options, output_dir, result.message)) {
    result.success = false;
    return false;
  }

  pcl::PointCloud<pcl::PointXYZ>::Ptr cloud(new pcl::PointCloud<pcl::PointXYZ>());
  if (!load_pcd_as_xyz(resolved_options.pcd_path, cloud, result.message)) {
    result.success = false;
    return false;
  }
  result.input_points = cloud->size();

  pcl::VoxelGrid<pcl::PointXYZ> voxel_filter;
  voxel_filter.setInputCloud(cloud);
  voxel_filter.setLeafSize(
    static_cast<float>(resolved_options.downsample_leaf_size),
    static_cast<float>(resolved_options.downsample_leaf_size),
    static_cast<float>(resolved_options.downsample_leaf_size));
  pcl::PointCloud<pcl::PointXYZ>::Ptr cloud_downsample(new pcl::PointCloud<pcl::PointXYZ>());
  voxel_filter.filter(*cloud_downsample);

  pcl::PointIndicesPtr ground_indices(new pcl::PointIndices());
  pcl::ProgressiveMorphologicalFilter<pcl::PointXYZ> pmf;
  pmf.setInputCloud(cloud_downsample);
  pmf.setMaxWindowSize(resolved_options.max_window_size);
  pmf.setSlope(resolved_options.slope);
  pmf.setInitialDistance(resolved_options.initial_distance);
  pmf.setMaxDistance(resolved_options.max_distance);
  pmf.extract(ground_indices->indices);

  pcl::PointCloud<pcl::PointXYZ>::Ptr cloud_ground(new pcl::PointCloud<pcl::PointXYZ>());
  pcl::PointCloud<pcl::PointXYZ>::Ptr cloud_nonground(new pcl::PointCloud<pcl::PointXYZ>());
  pcl::ExtractIndices<pcl::PointXYZ> extract_indices;
  extract_indices.setInputCloud(cloud_downsample);
  extract_indices.setIndices(ground_indices);
  extract_indices.setNegative(false);
  extract_indices.filter(*cloud_ground);
  extract_indices.setNegative(true);
  extract_indices.filter(*cloud_nonground);

  if (cloud_ground->empty()) {
    result.success = false;
    result.message = "No ground points detected. Adjust PMF parameters.";
    return false;
  }

  pcl::PointCloud<pcl::PointXYZ>::Ptr cloud_nonground_filtered(new pcl::PointCloud<pcl::PointXYZ>());
  pcl::StatisticalOutlierRemoval<pcl::PointXYZ> sor;
  sor.setInputCloud(cloud_nonground);
  sor.setMeanK(resolved_options.mean_k);
  sor.setStddevMulThresh(resolved_options.stddev_mul);
  sor.filter(*cloud_nonground_filtered);

  pcl::search::KdTree<pcl::PointXYZ>::Ptr kdtree(new pcl::search::KdTree<pcl::PointXYZ>());
  kdtree->setInputCloud(cloud_ground);

  pcl::PointCloud<pcl::PointXYZ>::Ptr cloud_obstacles(new pcl::PointCloud<pcl::PointXYZ>());
  cloud_obstacles->reserve(cloud_nonground_filtered->size());

  constexpr int kNearestGroundPoints = 12;
  std::vector<int> nearest_indices;
  std::vector<float> nearest_distances;

  for (const auto & point : cloud_nonground_filtered->points) {
    if (kdtree->nearestKSearch(point, kNearestGroundPoints, nearest_indices, nearest_distances) <= 0) {
      continue;
    }

    double ground_z = 0.0;
    int valid_ground_count = 0;
    for (const int index : nearest_indices) {
      if (index < 0 || static_cast<std::size_t>(index) >= cloud_ground->size()) {
        continue;
      }
      ground_z += cloud_ground->points[static_cast<std::size_t>(index)].z;
      ++valid_ground_count;
    }

    if (valid_ground_count == 0) {
      continue;
    }

    ground_z /= static_cast<double>(valid_ground_count);
    const double delta_z = static_cast<double>(point.z) - ground_z;
    if (delta_z >= resolved_options.h_min && delta_z <= resolved_options.h_max) {
      cloud_obstacles->push_back(point);
    }
  }

  result.obstacle_points = cloud_obstacles->size();
  if (!save_pgm_and_yaml(output_dir, resolved_options, cloud_obstacles, result)) {
    result.success = false;
    return false;
  }

  if (resolved_options.save_all_cloud &&
      !save_debug_clouds(
        output_dir, cloud_downsample, cloud_ground, cloud_nonground_filtered, cloud_obstacles,
        result.message)) {
    result.success = false;
    return false;
  }

  std::ostringstream summary;
  summary << "Generated Nav2 map from " << resolved_options.pcd_path
          << " -> " << result.pgm_path << ", " << result.yaml_path
          << " (input_points=" << result.input_points
          << ", obstacle_points=" << result.obstacle_points
          << ", size=" << result.width << "x" << result.height << ")";
  result.success = true;
  result.message = summary.str();
  return true;
}

}  // namespace agt_pcd2pgm
