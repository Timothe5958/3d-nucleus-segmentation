from dataclasses import dataclass


@dataclass
class ViewConfig:
    camera_rotation: tuple[float, float, float] = (95, 0, -70)
    mode: str = 'mip'
    is_label: bool = False
    cmap: str = 'cividis'
    voxel_size: float | None = None
    top_view: bool = False
