#include "agt_pcd2pgm/pcd_to_nav2_map.hpp"

#include <rclcpp/rclcpp.hpp>

class AgtPcd2PgmNode : public rclcpp::Node
{
public:
  AgtPcd2PgmNode()
  : Node("agt_pcd2pgm_node")
  {
    agt_pcd2pgm::ConversionOptions options;
    this->declare_parameter<std::string>("pcd_path", "");
    this->declare_parameter<std::string>("output_dir", "");
    this->declare_parameter<std::string>("save_map_name", "");
    this->declare_parameter<double>("resolution", options.resolution);
    this->declare_parameter<int>("min_points_per_cell", options.min_points_per_cell);
    this->declare_parameter<double>("h_min", options.h_min);
    this->declare_parameter<double>("h_max", options.h_max);
    this->declare_parameter<double>("downsample_leaf_size", options.downsample_leaf_size);
    this->declare_parameter<int>("max_window_size", options.max_window_size);
    this->declare_parameter<double>("slope", options.slope);
    this->declare_parameter<double>("initial_distance", options.initial_distance);
    this->declare_parameter<double>("max_distance", options.max_distance);
    this->declare_parameter<int>("mean_k", options.mean_k);
    this->declare_parameter<double>("stddev_mul", options.stddev_mul);
    this->declare_parameter<bool>("save_all_cloud", options.save_all_cloud);

    this->get_parameter("pcd_path", options.pcd_path);
    this->get_parameter("output_dir", options.output_dir);
    this->get_parameter("save_map_name", options.save_map_name);
    this->get_parameter("resolution", options.resolution);
    this->get_parameter("min_points_per_cell", options.min_points_per_cell);
    this->get_parameter("h_min", options.h_min);
    this->get_parameter("h_max", options.h_max);
    this->get_parameter("downsample_leaf_size", options.downsample_leaf_size);
    this->get_parameter("max_window_size", options.max_window_size);
    this->get_parameter("slope", options.slope);
    this->get_parameter("initial_distance", options.initial_distance);
    this->get_parameter("max_distance", options.max_distance);
    this->get_parameter("mean_k", options.mean_k);
    this->get_parameter("stddev_mul", options.stddev_mul);
    this->get_parameter("save_all_cloud", options.save_all_cloud);

    agt_pcd2pgm::ConversionResult result;
    if (agt_pcd2pgm::convert_pcd_to_nav2_map(options, result)) {
      RCLCPP_INFO(this->get_logger(), "%s", result.message.c_str());
    } else {
      RCLCPP_ERROR(this->get_logger(), "%s", result.message.c_str());
    }

    rclcpp::shutdown();
  }
};

int main(int argc, char ** argv)
{
  rclcpp::init(argc, argv);
  auto node = std::make_shared<AgtPcd2PgmNode>();
  (void)node;
  return 0;
}
