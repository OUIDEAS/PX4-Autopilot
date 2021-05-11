#pragma once

#include "FlightTask.hpp"

class FlightTaskHeadingControl : public FlightTask
{
public:
  FlightTaskHeadingControl() = default;
  virtual~FlightTaskHeadingControl() = default;

  bool update();
  bool activate(vehicle_local_position_setpoint_s last_setpoint);

private:
  float _origin_z{0.0f};
};

