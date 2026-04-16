# agt_pcd2pgm

`agt_pcd2pgm` converts a saved `.pcd` point-cloud map into a Nav2-compatible
`<name>.pgm` and `<name>.yaml`.

This package is adapted from the Apache-2.0 licensed upstream project
`kzm784/pcd2pgm` and integrated into the AGT workspace so FAST-LIO can trigger
map conversion automatically after saving a point-cloud map.

## Manual Run

```bash
cd /home/yangxuan/agt_navigation_stack/agt_ws
source install/setup.bash
ros2 run agt_pcd2pgm agt_pcd2pgm_node --ros-args \
  -p pcd_path:=/absolute/path/to/map.pcd \
  -p output_dir:=/absolute/path/to/output_dir \
  -p save_map_name:=map
```

When `output_dir` is empty, the generated map is written next to the source
`.pcd` file. When `save_map_name` is empty, the `.pcd` basename is reused.
