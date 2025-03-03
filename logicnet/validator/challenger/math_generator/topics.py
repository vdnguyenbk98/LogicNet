A = [
    ("power_rule_differentiation", "calculus"),
    ("basic_algebra", "algebra"),
    ("log", "algebra"),
    ("fraction_to_decimal", "basic_math"),
    ("multiply_int_to_22_matrix", "algebra"),
    ("area_of_triangle", "geometry"),
    ("valid_triangle", "geometry"),
    ("prime_factors", "misc"),
    ("pythagorean_theorem", "geometry"),
    ("linear_equations", "algebra"),
    ("prime_factors", "misc"),
    ("fraction_multiplication", "basic_math"),
    ("angle_regular_polygon", "geometry"),
    ("combinations", "statistics"),
    ("factorial", "basic_math"),
    ("surface_area_cube", "geometry"),
    ("surface_area_cuboid", "geometry"),
    ("surface_area_cylinder", "geometry"),
    ("volume_cube", "geometry"),
    ("volume_cuboid", "geometry"),
    ("volume_cylinder", "geometry"),
    ("surface_area_cone", "geometry"),
    ("volume_cone", "geometry"),
    ("common_factors", "misc"),
    ("intersection_of_two_lines", "algebra"),
    ("permutation", "statistics"),
    ("vector_cross", "algebra"),
    ("compare_fractions", "basic_math"),
    ("simple_interest", "algebra"),
    ("matrix_multiplication", "algebra"),
    ("cube_root", "basic_math"),
    ("power_rule_integration", "calculus"),
    ("fourth_angle_of_quadrilateral", "geometry"),
    ("quadratic_equation", "algebra"),
    ("dice_sum_probability", "statistics"),
    ("exponentiation", "basic_math"),
    ("confidence_interval", "statistics"),
    ("surds_comparison", "misc"),
    ("fibonacci_series", "computer_science"),
    ("basic_trigonometry", "geometry"),
    ("sum_of_polygon_angles", "geometry"),
    ("data_summary", "statistics"),
    ("surface_area_sphere", "geometry"),
    ("volume_sphere", "geometry"),
    ("nth_fibonacci_number", "computer_science"),
    ("profit_loss_percent", "misc"),
    ("binary_to_hex", "computer_science"),
    ("multiply_complex_numbers", "algebra"),
    ("geometric_progression", "misc"),
    ("geometric_mean", "misc"),
    ("harmonic_mean", "misc"),
    ("euclidian_norm", "misc"),
    ("angle_btw_vectors", "geometry"),
    ("absolute_difference", "basic_math"),
    ("vector_dot", "algebra"),
    ("binary_2s_complement", "computer_science"),
    ("invert_matrix", "algebra"),
    ("sector_area", "geometry"),
    ("mean_median", "statistics"),
    ("int_matrix_22_determinant", "algebra"),
    ("compound_interest", "algebra"),
    ("decimal_to_hexadeci", "computer_science"),
    ("percentage", "basic_math"),
    ("celsius_to_fahrenheit", "misc"),
    ("arithmetic_progression_term", "misc"),
    ("arithmetic_progression_sum", "misc"),
    ("decimal_to_octal", "computer_science"),
    ("decimal_to_roman_numerals", "misc"),
    ("degree_to_rad", "geometry"),
    ("radian_to_deg", "geometry"),
    ("trig_differentiation", "calculus"),
    ("definite_integral", "calculus"),
    ("is_prime", "basic_math"),
    ("complex_to_polar", "misc"),
    ("set_operation", "misc"),
    ("base_conversion", "misc"),
    ("curved_surface_area_cylinder", "geometry"),
    ("perimeter_of_polygons", "geometry"),
    ("power_of_powers", "basic_math"),
    ("quotient_of_power_same_base", "misc"),
    ("quotient_of_power_same_power", "misc"),
    ("complex_quadratic", "algebra"),
    ("is_leap_year", "misc"),
    ("minutes_to_hours", "misc"),
    ("circumference", "geometry"),
    ("combine_like_terms", "algebra"),
    ("signum_function", "misc"),
    ("conditional_probability", "statistics"),
    ("arc_length", "geometry"),
    ("stationary_points", "calculus"),
    ("expanding", "algebra"),
    ("area_of_circle", "geometry"),
    ("volume_cone_frustum", "geometry"),
    ("equation_of_line_from_two_points", "geometry"),
    ("area_of_circle_given_center_and_point", "geometry"),
    ("factors", "misc"),
    ("volume_hemisphere", "geometry"),
    ("percentage_difference", "basic_math"),
    ("percentage_error", "basic_math"),
    ("greatest_common_divisor", "basic_math"),
    ("product_of_scientific_notations", "misc"),
    ("volume_pyramid", "geometry"),
    ("surface_area_pyramid", "geometry"),
    ("is_composite", "basic_math"),
    ("complementary_and_supplementary_angle", "geometry"),
    ("simplify_square_root", "basic_math"),
    ("line_equation_from_2_points", "algebra"),
    ("orthogonal_projection", "algebra"),
    ("area_of_trapezoid", "geometry"),
    # ("tribonacci_series", "computer_science"),
    ("nth_tribonacci_number", "computer_science"),
    ("velocity_of_object", "misc"),
]
TOPICS = [dict(topic=topic, subtopic=subtopic) for subtopic, topic in A]


if __name__ == "__main__":
    import mathgenerator
    from latex2sympy2 import latex2sympy

    print(mathgenerator)
    for topic in TOPICS:
        subtopic = topic["subtopic"]
        topic = topic["topic"]
        print(f"Topic: {topic}, Subtopic: {subtopic}")
        atom_problem, atom_answer = eval(f"mathgenerator.{topic}.{subtopic}()")
        print(f"Topic: {topic}, Subtopic: {subtopic}")
        print(f"Generated atom math problem: {atom_problem}")
        print(f"Answer: {atom_answer}")
        atom_answer = atom_answer.replace("$", "").replace("=", "").strip()
        try:
            atom_answer = latex2sympy(atom_answer)
            print(f"Sympy Answer: {atom_answer}")
            print(type(atom_answer))
        except Exception:
            try:
                atom_answer = atom_answer.replace("$", "").replace("=", "").strip()
                atom_answer = eval(atom_answer)
                print(f"Python Answer: {atom_answer}")
            except Exception as e:
                print(f"Error: {e}")
        print("--" * 10)
