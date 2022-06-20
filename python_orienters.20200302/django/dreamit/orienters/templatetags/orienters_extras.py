from django import template
from random import randint

register = template.Library()

@register.filter
def commatize(value, arg):
    """Removes all values of arg from the given string"""
    return value.replace(arg, ', ')

@register.filter
def addstr(arg1, arg2):
    """concatenate arg1 & arg2"""
    return str(arg1) + str(arg2)

@register.filter
def g_e_a_i(arrey, key):
    """get element at index"""
    return arrey[key]

@register.simple_tag
def v_f_p_a_x_y(arrey, x, y, property):
    """value for property at x & y"""
    return getattr(arrey[x][y], property, '')

@register.simple_tag
def i_m_i_p_o(index, increment, offset):
    """index multiplied with increment plus offset"""
    return (index * increment) + offset

@register.simple_tag
def construct_static_image_url(arrey, index):
    return '/static/img/' + arrey[int(index) + 0]

@register.simple_tag
def construct_pdf_static_image_url(prefix, arrey, index):
    return prefix + '/img/' + arrey[int(index) + 0]

@register.simple_tag
def proper_reflector_name(rns):
    return "-".join(rn.capitalize() for rn in rns.split("|"))

@register.simple_tag
def extract_answer(db_results, cadence, eendex):
    """get value for property"""
    for db_result in db_results:
        # if db_result.get('cadence') == cadence.lower():
        if db_result.cadence == cadence.lower():
            # if db_result.get('index') == eendex:
            if db_result.iindex == eendex:
                # return db_result.get('text')
                return db_result.text
            else:
                continue
        else:
            continue

    return ''
