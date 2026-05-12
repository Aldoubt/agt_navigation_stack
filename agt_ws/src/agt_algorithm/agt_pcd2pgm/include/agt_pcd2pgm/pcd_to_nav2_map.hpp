#ifndef AGT_PCD2PGM__PCD_TO_NAV2_MAP_HPP_
#define AGT_PCD2PGM__PCD_TO_NAV2_MAP_HPP_

#include <string>

namespace agt_pcd2pgm
{

struct ConversionOptions
{
  std::string pcd_path;
  std::string output_dir;
  std::string save_map_name;
  double resolution = 0.10;
  int min_points_per_cell = 1;
  double h_min = 0.10;
  double h_max = 1.50;
  double downsample_leaf_size = 0.25;
  int max_window_size = 32;
  double slope = 1.0;
  double initial_distance = 0.3;
  double max_distance = 2.5;
  int mean_k = 20;
  double stddev_mul = 1.0;
  bool save_all_cloud = false;
};

struct ConversionResult
{
  bool success = false;
  std::string message;
  std::string pgm_path;
  std::string yaml_path;
  std::size_t input_points = 0;
  std::size_t obstacle_points = 0;
  int width = 0;
  int height = 0;
};

bool convert_pcd_to_nav2_map(const ConversionOptions & options, ConversionResult & result);

}  // namespace agt_pcd2pgm

#endif  // AGT_PCD2PGM__PCD_TO_NAV2_MAP_HPP_
