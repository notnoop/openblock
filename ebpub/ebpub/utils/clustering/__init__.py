from ebpub.utils.mapmath import get_resolution, lnglat_from_px, px_from_lnglat
from ebpub.utils.clustering import cluster
from django.conf import settings

def cluster_by_scale(objs, radius, scale, extent=(-180, -90, 180, 90),
                     cluster_fn=cluster.buffer_cluster):
    """
    Required parameters:

        + objs: dict, keys to ID objects, values are point 2-tuples
        + radius: in pixels
        + scale: a map scale - the 'n' in '1/n', eg., 19200

    Returns a list of bunches.
    """
    resolution = get_resolution(scale)

    # Translate from lng/lat into coordinate system of the display.
    objs = dict([(k, px_from_lnglat(v, resolution, extent)) for k, v in objs.iteritems()])

    bunches = []
    for bunch in cluster_fn(objs, radius):
        # Translate back into lng/lat.
        bunch.center = lnglat_from_px(bunch.center, resolution, extent)
        bunches.append(bunch)

    return bunches

def cluster_scales(objs, radius, scales=settings.MAP_SCALES, extent=(-180, -90, 180, 90),
                   cluster_fn=cluster.buffer_cluster):
    """
    Required parameters:

        + objs: dict, keys to ID objects, values are point 2-tuples
        + radius: in pixels
        + scales: map scales - the 'n' in '1/n', eg., 19200

    Returns: mapping of scale -> list of clusters for that scale
    """
    return dict([(scale, cluster_by_scale(objs, radius, scale, extent, cluster_fn))
                 for scale in scales])
