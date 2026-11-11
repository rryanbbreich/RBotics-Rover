"""
RoverSkeleton - Fusion 360 script

Creates the rover's user parameters and a 'Skeleton' component holding two
layout sketches for a six-wheel rocker-bogie rover:
  - Side layout (XZ): ground, wheels, rocker and bogie links, pivots, body
  - Top layout (XY): wheel footprints, body outline, pivot axes

Workflow:
  1. Run once to create the parameters and skeleton.
  2. Edit values in Modify > Change Parameters.
  3. Re-run to regenerate the skeleton from the new values.
Existing parameter values are kept on re-run unless RESET_PARAMS = True.

Axes: +X forward, +Y left, +Z up. Ground at Z = 0, middle wheel axle at X = 0.
"""

import adsk.core
import adsk.fusion
import traceback

RESET_PARAMS = False
SKELETON_NAME = 'Skeleton'

# (name, expression, units, comment)
PARAMS = [
    ('wheel_d',          '60 mm',  'mm', 'Wheel outer diameter'),
    ('wheel_w',          '25 mm',  'mm', 'Wheel width'),
    ('wheel_pitch',      '100 mm', 'mm', 'Axle spacing front-middle and middle-rear'),
    ('track_w',          '240 mm', 'mm', 'Wheel centre to wheel centre, left-right'),
    ('bogie_pivot_h',    '35 mm',  'mm', 'Bogie pivot height above axle line'),
    ('rocker_pivot_h',   '65 mm',  'mm', 'Rocker pivot height above axle line'),
    ('rocker_pivot_x',   '50 mm',  'mm', 'Rocker pivot X position, forward of middle axle'),
    ('body_clearance',   '50 mm',  'mm', 'Ground to underside of body'),
    ('body_len',         '250 mm', 'mm', 'Body length'),
    ('body_w',           '140 mm', 'mm', 'Body width'),
    ('body_h',           '70 mm',  'mm', 'Body height'),
    ('pivot_bore',       '5 mm',   'mm', '625ZZ bearing bore / M5 axle'),
    ('pivot_bearing_od', '16 mm',  'mm', '625ZZ bearing outer diameter'),
    ('pivot_bearing_w',  '5 mm',   'mm', '625ZZ bearing width'),
    ('n20_w',            '12 mm',  'mm', 'N20 gearbox width'),
    ('n20_h',            '10 mm',  'mm', 'N20 gearbox height'),
    ('n20_shaft_d',      '3 mm',   'mm', 'N20 D-shaft diameter'),
    # Link / part parameters
    ('arm_w',            '14 mm',  'mm', 'Rocker/bogie arm width (in side view)'),
    ('arm_t',            '8 mm',   'mm', 'Rocker/bogie arm thickness (Y direction)'),
    ('arm_gap',          '2 mm',   'mm', 'Clearance between body side and rocker'),
    ('fit_press',        '0.15 mm', 'mm', 'Bearing seat interference allowance (tune with test print)'),
    ('fit_clear',        '0.3 mm', 'mm', 'Clearance for sliding/bolt fits'),
]


def ensure_params(design):
    up = design.userParameters
    for name, expr, units, comment in PARAMS:
        p = up.itemByName(name)
        if p is None:
            up.add(name, adsk.core.ValueInput.createByString(expr), units, comment)
        elif RESET_PARAMS:
            p.expression = expr


def read_params(design):
    # Values come back in Fusion internal units (cm)
    up = design.userParameters
    return {name: up.itemByName(name).value for name, _, _, _ in PARAMS}


def remove_old_skeleton(root):
    occs = root.occurrences
    for i in range(occs.count - 1, -1, -1):
        occ = occs.item(i)
        if occ.component.name == SKELETON_NAME:
            occ.deleteMe()


def pt(sketch, x, y, z):
    # Convert model coordinates to sketch space so 'up' is always +Z,
    # regardless of how Fusion orients the XZ plane's sketch axes.
    return sketch.modelToSketchSpace(adsk.core.Point3D.create(x, y, z))


def draw_side(comp, d):
    sk = comp.sketches.add(comp.xZConstructionPlane)
    sk.name = 'Side layout (XZ)'
    lines = sk.sketchCurves.sketchLines
    circles = sk.sketchCurves.sketchCircles

    r = d['wheel_d'] / 2
    pitch = d['wheel_pitch']
    xf, xm, xr = pitch, 0.0, -pitch
    axle_z = r
    bogie_x, bogie_z = -pitch / 2, axle_z + d['bogie_pivot_h']
    rocker_x, rocker_z = d['rocker_pivot_x'], axle_z + d['rocker_pivot_h']

    # Ground reference
    ground = lines.addByTwoPoints(pt(sk, xr - r - 2, 0, 0), pt(sk, xf + r + 2, 0, 0))
    ground.isConstruction = True

    # Wheels
    front = circles.addByCenterRadius(pt(sk, xf, 0, axle_z), r)
    middle = circles.addByCenterRadius(pt(sk, xm, 0, axle_z), r)
    rear = circles.addByCenterRadius(pt(sk, xr, 0, axle_z), r)

    # Rocker: front axle -> rocker pivot -> bogie pivot
    rocker_a = lines.addByTwoPoints(front.centerSketchPoint, pt(sk, rocker_x, 0, rocker_z))
    rocker_b = lines.addByTwoPoints(rocker_a.endSketchPoint, pt(sk, bogie_x, 0, bogie_z))

    # Bogie: middle axle -> bogie pivot -> rear axle
    lines.addByTwoPoints(middle.centerSketchPoint, rocker_b.endSketchPoint)
    lines.addByTwoPoints(rocker_b.endSketchPoint, rear.centerSketchPoint)

    # Pivot bearing outlines
    circles.addByCenterRadius(rocker_a.endSketchPoint, d['pivot_bearing_od'] / 2)
    circles.addByCenterRadius(rocker_b.endSketchPoint, d['pivot_bearing_od'] / 2)

    # Body envelope (construction)
    z0 = d['body_clearance']
    z1 = z0 + d['body_h']
    half_len = d['body_len'] / 2
    body = lines.addTwoPointRectangle(pt(sk, -half_len, 0, z0), pt(sk, half_len, 0, z1))
    for i in range(body.count):
        body.item(i).isConstruction = True

    return sk


def draw_top(comp, d):
    sk = comp.sketches.add(comp.xYConstructionPlane)
    sk.name = 'Top layout (XY)'
    lines = sk.sketchCurves.sketchLines

    r = d['wheel_d'] / 2
    pitch = d['wheel_pitch']
    half_track = d['track_w'] / 2
    half_ww = d['wheel_w'] / 2

    # Wheel footprints, both sides
    for x in (pitch, 0.0, -pitch):
        for side in (1, -1):
            y = side * half_track
            lines.addTwoPointRectangle(pt(sk, x - r, y - half_ww, 0),
                                       pt(sk, x + r, y + half_ww, 0))

    # Body outline
    half_len = d['body_len'] / 2
    half_bw = d['body_w'] / 2
    lines.addTwoPointRectangle(pt(sk, -half_len, -half_bw, 0), pt(sk, half_len, half_bw, 0))

    # Pivot axes across the rover (construction)
    for x in (d['rocker_pivot_x'], -pitch / 2):
        axis = lines.addByTwoPoints(pt(sk, x, -half_track, 0), pt(sk, x, half_track, 0))
        axis.isConstruction = True

    # Centreline (construction)
    cl = lines.addByTwoPoints(pt(sk, -half_len - 2, 0, 0), pt(sk, half_len + 2, 0, 0))
    cl.isConstruction = True

    return sk


def sanity_report(d):
    mm = lambda v: v * 10.0
    r = d['wheel_d'] / 2
    rocker_z = r + d['rocker_pivot_h']
    body_top = d['body_clearance'] + d['body_h']
    side_gap = d['track_w'] / 2 - d['wheel_w'] / 2 - d['body_w'] / 2
    overall_len = 2 * d['wheel_pitch'] + d['wheel_d']
    overall_w = d['track_w'] + d['wheel_w']

    lines = [
        'Skeleton generated.',
        '',
        'Overall footprint: {:.0f} x {:.0f} mm (L x W)'.format(mm(max(overall_len, d['body_len'])), mm(overall_w)),
        'Body-to-wheel side gap (for arms + motors): {:.1f} mm'.format(mm(side_gap)),
        'Rocker pivot height above ground: {:.0f} mm'.format(mm(rocker_z)),
    ]
    warnings = []
    if side_gap < 2.5:
        warnings.append('Side gap under 25 mm: little room for rocker arms and N20 motors.')
    if not (d['body_clearance'] < rocker_z < body_top):
        warnings.append('Rocker pivot is outside the body height range; it has nothing to mount to.')
    if d['body_len'] / 2 > d['wheel_pitch'] + r:
        warnings.append('Body overhangs the front/rear wheels.')
    if warnings:
        lines += ['', 'Warnings:'] + ['- ' + w for w in warnings]
    return '\n'.join(lines)


def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        design = adsk.fusion.Design.cast(app.activeProduct)
        if not design:
            ui.messageBox('Open a Fusion design first (Design workspace).')
            return

        if design.designType != adsk.fusion.DesignTypes.ParametricDesignType:
            design.designType = adsk.fusion.DesignTypes.ParametricDesignType

        ensure_params(design)
        d = read_params(design)

        root = design.rootComponent
        remove_old_skeleton(root)
        occ = root.occurrences.addNewComponent(adsk.core.Matrix3D.create())
        comp = occ.component
        comp.name = SKELETON_NAME

        draw_side(comp, d)
        draw_top(comp, d)

        ui.messageBox(sanity_report(d), 'Rover Skeleton')
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
