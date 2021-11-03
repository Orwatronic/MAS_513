
"use strict";

let MasterboardDataMsg = require('./MasterboardDataMsg.js');
let Digital = require('./Digital.js');
let RobotStateRTMsg = require('./RobotStateRTMsg.js');
let Analog = require('./Analog.js');
let RobotModeDataMsg = require('./RobotModeDataMsg.js');
let ToolDataMsg = require('./ToolDataMsg.js');
let IOStates = require('./IOStates.js');

module.exports = {
  MasterboardDataMsg: MasterboardDataMsg,
  Digital: Digital,
  RobotStateRTMsg: RobotStateRTMsg,
  Analog: Analog,
  RobotModeDataMsg: RobotModeDataMsg,
  ToolDataMsg: ToolDataMsg,
  IOStates: IOStates,
};
