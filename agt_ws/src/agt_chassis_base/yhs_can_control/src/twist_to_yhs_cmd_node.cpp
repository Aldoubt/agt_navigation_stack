#include <algorithm>
#include <cmath>
#include <cstdint>
#include <functional>
#include <memory>
#include <string>

#include "geometry_msgs/msg/twist.hpp"
#include "rclcpp/rclcpp.hpp"
#include "yhs_can_interfaces/msg/ctrl_cmd.hpp"

namespace yhs
{

class TwistToYhsCmdNode final : public rclcpp::Node
{
public:
  TwistToYhsCmdNode() : Node("twist_to_yhs_cmd_node")
  {
    input_twist_topic_ = declare_parameter<std::string>("input_twist_topic", "/cmd_vel");
    output_ctrl_cmd_topic_ = declare_parameter<std::string>("output_ctrl_cmd_topic", "/ctrl_cmd");
    max_linear_velocity_ = declare_parameter<double>("max_linear_velocity", 0.8);
    max_angular_velocity_ = declare_parameter<double>("max_angular_velocity", 1.0);
    steering_gain_ = declare_parameter<double>("steering_gain", 1.0);
    cmd_timeout_sec_ = declare_parameter<double>("cmd_timeout_sec", 0.3);
    publish_rate_hz_ = declare_parameter<double>("publish_rate_hz", 20.0);
    linear_deadband_ = declare_parameter<double>("linear_deadband", 0.01);
    angular_deadband_ = declare_parameter<double>("angular_deadband", 0.01);
    allow_reverse_ = declare_parameter<bool>("allow_reverse", false);
    forward_gear_ = static_cast<uint8_t>(declare_parameter<int>("forward_gear", 1));
    reverse_gear_ = static_cast<uint8_t>(declare_parameter<int>("reverse_gear", 2));
    neutral_gear_ = static_cast<uint8_t>(declare_parameter<int>("neutral_gear", 0));
    startup_neutral_publish_ = declare_parameter<bool>("startup_neutral_publish", true);

    ctrl_pub_ = create_publisher<yhs_can_interfaces::msg::CtrlCmd>(output_ctrl_cmd_topic_, 10);
    twist_sub_ = create_subscription<geometry_msgs::msg::Twist>(
      input_twist_topic_, 20,
      std::bind(&TwistToYhsCmdNode::twistCallback, this, std::placeholders::_1));

    const auto period = std::chrono::duration<double>(1.0 / std::max(1.0, publish_rate_hz_));
    timer_ = create_wall_timer(
      std::chrono::duration_cast<std::chrono::nanoseconds>(period),
      std::bind(&TwistToYhsCmdNode::publishCmd, this));

    if (startup_neutral_publish_) {
      publishNeutral();
    }

    RCLCPP_INFO(
      get_logger(),
      "twist_to_yhs_cmd started: %s -> %s, vmax=%.2f m/s, wmax=%.2f rad/s, timeout=%.2fs, "
      "allow_reverse=%s",
      input_twist_topic_.c_str(), output_ctrl_cmd_topic_.c_str(), max_linear_velocity_,
      max_angular_velocity_, cmd_timeout_sec_, allow_reverse_ ? "true" : "false");
  }

private:
  void twistCallback(const geometry_msgs::msg::Twist::SharedPtr msg)
  {
    last_twist_ = *msg;
    last_twist_time_ = now();
    has_cmd_ = true;
  }

  void publishNeutral()
  {
    yhs_can_interfaces::msg::CtrlCmd out;
    out.ctrl_cmd_gear = neutral_gear_;
    out.ctrl_cmd_velocity = 0.0F;
    out.ctrl_cmd_steering = 0.0F;
    ctrl_pub_->publish(out);
  }

  void publishCmd()
  {
    if (!has_cmd_ || (now() - last_twist_time_).seconds() > cmd_timeout_sec_) {
      publishNeutral();
      return;
    }

    double linear = std::clamp(last_twist_.linear.x, -max_linear_velocity_, max_linear_velocity_);
    double angular =
      std::clamp(last_twist_.angular.z, -max_angular_velocity_, max_angular_velocity_);

    if (std::abs(linear) < linear_deadband_) {
      linear = 0.0;
    }
    if (std::abs(angular) < angular_deadband_) {
      angular = 0.0;
    }

    yhs_can_interfaces::msg::CtrlCmd out;
    if (linear > 0.0) {
      out.ctrl_cmd_gear = forward_gear_;
      out.ctrl_cmd_velocity = static_cast<float>(linear);
    } else if (linear < 0.0 && allow_reverse_) {
      out.ctrl_cmd_gear = reverse_gear_;
      out.ctrl_cmd_velocity = static_cast<float>(std::abs(linear));
    } else {
      out.ctrl_cmd_gear = neutral_gear_;
      out.ctrl_cmd_velocity = 0.0F;
    }
    out.ctrl_cmd_steering = static_cast<float>(angular * steering_gain_);
    ctrl_pub_->publish(out);
  }

  std::string input_twist_topic_;
  std::string output_ctrl_cmd_topic_;
  double max_linear_velocity_{0.8};
  double max_angular_velocity_{1.0};
  double steering_gain_{1.0};
  double cmd_timeout_sec_{0.3};
  double publish_rate_hz_{20.0};
  double linear_deadband_{0.01};
  double angular_deadband_{0.01};
  bool allow_reverse_{false};
  uint8_t forward_gear_{1};
  uint8_t reverse_gear_{2};
  uint8_t neutral_gear_{0};
  bool startup_neutral_publish_{true};

  bool has_cmd_{false};
  geometry_msgs::msg::Twist last_twist_;
  rclcpp::Time last_twist_time_{0, 0, RCL_ROS_TIME};

  rclcpp::Publisher<yhs_can_interfaces::msg::CtrlCmd>::SharedPtr ctrl_pub_;
  rclcpp::Subscription<geometry_msgs::msg::Twist>::SharedPtr twist_sub_;
  rclcpp::TimerBase::SharedPtr timer_;
};

}  // namespace yhs

int main(int argc, char ** argv)
{
  rclcpp::init(argc, argv);
  auto node = std::make_shared<yhs::TwistToYhsCmdNode>();
  rclcpp::spin(node);
  rclcpp::shutdown();
  return 0;
}
