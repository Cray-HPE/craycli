// Copyright 2019 Cray Inc. All Rights Reserved.

@Library("dst-shared@release/shasta-1.3") _

rpmBuild(
    fanout_params: ["sle15sp1"],
    channel: "casm-cloud-alerts",
    slack_notify: ['FAILURE'],
    product: "shasta-standard,shasta-premium",
    arch: "noarch",
    target_node: "ncn,cn"
)
