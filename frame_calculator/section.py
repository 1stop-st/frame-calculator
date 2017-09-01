"""Calculate cross-sectional coefficients.

This module provides functions to calculate cross-sectional coefficients, such as area, inertia, etc.
Usually, `convert` function is just you need to convert raw parameter collections to useful coefficient collections.

Example
-------
(TODO) calculation example.
"""
from math import pi, sqrt
from copy import deepcopy


def convert(section_parameters):
    """Convert raw section parameters to calculated coefficients.

    Calculate structural coefficients of section. Argument dictionary will be parsed according to its shape.
    Following shapes and functions are acceptable and used to calculate return values.

    - 'H' : :func:`frame_calculator.section.h`
    - 'I' : :func:`frame_calculator.section.i`
    - 'O' : :func:`frame_calculator.section.o`

    Parameters
    ----------
    section_parameters : dict
        Section's shape and size. Must have 'shape' key and parameters corresponding the shape.

    Returns
    -------
    dict
        Section's coefficients.
    """
    shape = section_parameters.pop('shape')
    if shape == 'H':
        return h(**section_parameters)
    elif shape == 'T':
        return t(**section_parameters)
    elif shape == 'I':
        return i(**section_parameters)
    elif shape == 'O':
        return o(**section_parameters)
    elif shape == 'C':
        return c(**section_parameters)
    elif shape == 'R':
        return r(**section_parameters)


def properties(shape, **kwargs):
    """Proxy to convert.

    Shape and other parameters are mixed in one dictionary.

    Parameters
    ---------
    shape : str
        String represents section's shape.
    **kwargs
        Parameters.

    Returns
    -------
    dict
        Section's coefficients.
    """
    kwargs['shape'] = shape
    return convert(kwargs)


def h(H, B, tw, tf, r=0):
    """Calculate cross-sectional coefficients of H section.

    H section is commonly used as horizontal steel beams.

    Parameters
    ----------
    H : float
        Height, or distance between the outedge of flanges.
    B : float
        Breadth or width of the flanges.
    tw : float
        Thickness of the web.
    tf : float
        Thickness of the flanges. 2 flanges are assumed to have same thickness.
    r : float, optional
        Radius of fillets. 4 fillets are assumed to have same radius.

    Returns
    -------
    dict(str, float)
        Dictionary having calculated cross-sectional coefficients.::

            {
                'Ax': Cross-sectional area,
                'Ay': Cross-sectional area of the web,
                'Az': Cross-sectional area of flanges (total),
                'Iy': Moment of inertia around y-axis,
                'Iz': Moment of inertia around z-axis,
                'J': Polor moment of area,
                'Zy': Elastic section modulus around y-axis,
                'Zz': Elastic section modulus around z-axis,
                'iy': Radius of gyration around y-axis,
                'iz': Radius of gyration around z-axis
            }

        In this context,
            - x-axis direction is axial direction.
            - y-axis direction is weak-axis (parallels flanges) direction.
            - z-axis direction is strong-axis (parallels web) direction.
    """
    rd = (1 - 2 / (4 - pi) / 3) * r
    rA = (1 - pi * 0.25) * r ** 2
    rI = (1 / 3. - pi / 16 - 1 / (4 - pi) / 9) * r ** 4
    A = B * tf * 2 + (H - tf * 2) * tw + rA * 4
    tIf = tf * B * B * B / 12.
    tIw = (H - tf * 2) * tw * tw * tw / 12.
    tIr = rI + rA * ((tw * 0.25 + rd) * tw + rd * rd)
    Iz = tIf * 2 + tIw + tIr * 4
    tIf = B * tf ** 3 / 12. + B * tf * (H - tf) ** 2 * 0.25
    tIw = tw * (H - tf * 2) ** 3 / 12.
    tIr = rI + rA * (H * 0.5 - tf - rd) ** 2
    Iy = tIf * 2 + tIw + tIr * 4
    return {
        'Ax': A,
        'Ay': float(tf * B * 2),
        'Az': float(tw * H),
        'Iy': Iy,
        'Iz': Iz,
        'J': (B * tf ** 3 * 2 + (H - tf * 2) * tw ** 3) / 3.,
        'Zy': Iy / H * 2,
        'Zz': Iz / B * 2,
        'iy': sqrt(Iy / A),
        'iz': sqrt(Iz / A)
    }


def t(H, B, tw, tf, r=0):
    """Calculate cross-sectional coefficients of T section.

    T section is like cut off H section.

    Parameters
    ----------
    H : float
        Height, or distance between outedge of the flange and the tip of the web.
    B : float
        Breadth or width of the flange.
    tw : float
        Thickness of the web.
    tf : float
        Thickness of the flange.
    r : float, optional
        Radius of fillets. 2 fillets are assumed to have same radius.

    Returns
    -------
    dict(str, float)
        Dictionary having calculated cross-sectional coefficients.::

            {
                'Ax': Cross-sectional area,
                'Ay': Cross-sectional area of the web,
                'Az': Cross-sectional area of the flange,
                'Iy': Moment of inertia around y-axis,
                'Iz': Moment of inertia around z-axis,
                'Zy': Elastic section modulus around y-axis,
                'Zz': Elastic section modulus around z-axis,
                'iy': Radius of gyration around y-axis,
                'iz': Radius of gyration around z-axis,
                'Cz': Distance between the outedge of the flange and the centroid.
            }

        In this context,
            - x-axis direction is axial direction.
            - y-axis direction is weak-axis (parallels flanges) direction.
            - z-axis direction is strong-axis (parallels web) direction.
    """
    rd = (1 - 2 / (4 - pi) / 3) * r
    rA = (1 - pi * 0.25) * r ** 2
    rI = (1 / 3. - pi / 16 - 1 / (4 - pi) / 9) * r ** 4
    A = B * tf + (H - tf) * tw + rA * 2
    Sy = ((B - tw) * tf * tf + H * H * tw) * 0.5 + rA * (tf + rd) * 2
    Cy = Sy / A
    tIf = tf * B * B * B / 12.
    tIw = (H - tf) * tw * tw * tw / 12.
    tIr = rI + rA * (tw * 0.5 + rd) ** 2
    Iz = tIf + tIw + tIr * 2
    tIf = B * tf * tf * tf / 12. + B * tf * (Cy - tf * 0.5) ** 2
    tIw = tw * (H - tf) ** 3 / 12. + tw * (H - tf) * ((H + tf) * 0.5 - Cy) ** 2
    tIr = rI + rA * (Cy - tf - rd) ** 2
    Iy = tIf + tIw + tIr * 2
    return {
        'Ax': A,
        'Ay': float(tf * B),
        'Az': float(tw * H),
        'Iy': Iy,
        'Iz': Iz,
        'Zy': Iy / max(Cy, H - Cy),
        'Zz': Iz / B * 2,
        'iy': sqrt(Iy / A),
        'iz': sqrt(Iz / A),
        'Cz': Cy
    }


def o(D, t=0):
    """Calculate cross-sectional coefficients of circle and pipe section.

    The outedge of section is assumed to be a perfect circle.

    Parameters
    ----------
    D : float
        Diameter.
    t : float, optional
        Thickness. If t = 0, the section is considered as filled circle. Othewise as hollow.

    Returns
    -------
    dict(str, float)
        Dictionary having calculated cross-sectional coefficients.::

            {
                'Ax': Cross-sectional area,
                'Iy': Moment of inertia around y-axis,
                'Iz': Moment of inertia around z-axis,
                'Zy': Elastic section modulus around y-axis,
                'Zz': Elastic section modulus around z-axis,
                'iy': Radius of gyration around y-axis,
                'iz': Radius of gyration around z-axis,
                'J': Polor moment of area
            }

        In this context, x-axis direction is axial direction.
    """
    A = 0.25 * D ** 2 * pi
    I = 0.015625 * D ** 4 * pi
    if t:
        A -= 0.25 * (D - t) ** 2 * pi
        I -= 0.015625 * (D - t) ** 2 * pi
    Z = 0.5 * I / D
    i = sqrt(I / A)
    return {
        'Ax': A,
        'Iy': I,
        'Iz': I,
        'Zy': Z,
        'Zz': Z,
        'iy': i,
        'iz': i,
        'J': I * 2.
    }
