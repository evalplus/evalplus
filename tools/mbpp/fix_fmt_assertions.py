import json

original_path = "MbppPlus-OriginFmt-v0.1.0.jsonl"
fixed_path = "MbppPlus-OriginFmt-v0.1.0_fixed.jsonl"


def change_dataset():
    Mbpp = {}
    with open(original_path, "r") as f:
        for line in f:
            data = json.loads(line)
            Mbpp[data["task_id"]] = data

    # Fix 164
    assert Mbpp[164]["test_list"][2] == "assert are_equivalent(23, 47) == True"
    Mbpp[164]["test_list"][2] = "assert are_equivalent(23, 47) == False"

    # Fix 143
    assert (
        Mbpp[143]["test_list"][2]
        == "assert find_lists(([9, 8, 7, 6, 5, 4, 3, 2, 1])) == 1"
    )
    Mbpp[143]["test_list"][
        2
    ] = "assert find_lists(([9, 8, 7, 6, 5, 4, 3, 2, 1], )) == 1"

    # Fix 229
    assert (
        Mbpp[229]["test_list"][0]
        == "assert re_arrange_array([-1, 2, -3, 4, 5, 6, -7, 8, 9], 9) == [-1, -3, -7, 4, 5, 6, 2, 8, 9]"
    )
    Mbpp[229]["test_list"][
        0
    ] = "assert re_arrange_array([-1, 2, -3, 4, 5, 6, -7, 8, 9], 9) == [-1, -3, -7, 2, 4, 5, 6, 8, 9]"

    # Fix 407
    assert Mbpp[407]["test_list"][1] == "assert rearrange_bigger(10)==False"
    Mbpp[407]["test_list"][1] = "assert rearrange_bigger(10)==None"

    # Fix 431
    assert (
        Mbpp[431]["test_list"][1]
        == "assert common_element([1,2,3,4,5], [6,7,8,9])==None"
    )
    Mbpp[431]["test_list"][1] = "assert common_element([1,2,3,4,5], [6,7,8,9])==False"

    # Fix 438
    assert (
        Mbpp[438]["test_list"][2]
        == "assert count_bidirectional([(5, 6), (1, 2), (6, 5), (9, 2), (6, 5), (2, 1)] ) == 4"
    )
    Mbpp[438]["test_list"][
        2
    ] = "assert count_bidirectional([(5, 6), (1, 2), (6, 5), (9, 2), (6, 5), (2, 1)]) == 3.0"

    # Fix 442
    assert len(Mbpp[442]["test_imports"]) == 0
    Mbpp[442]["test_imports"].append("import math")
    assert (
        Mbpp[442]["test_list"][0]
        == "assert positive_count([0, 1, 2, -1, -5, 6, 0, -3, -2, 3, 4, 6, 8])==0.54"
    )
    assert (
        Mbpp[442]["test_list"][1]
        == "assert positive_count([2, 1, 2, -1, -5, 6, 4, -3, -2, 3, 4, 6, 8])==0.69"
    )
    assert (
        Mbpp[442]["test_list"][2]
        == "assert positive_count([2, 4, -6, -9, 11, -12, 14, -5, 17])==0.56"
    )
    Mbpp[442]["test_list"][
        0
    ] = "assert positive_count([0, 1, 2, -1, -5, 6, 0, -3, -2, 3, 4, 6, 8]) == 0.5384615384615384"
    Mbpp[442]["test_list"][
        1
    ] = "assert positive_count([2, 1, 2, -1, -5, 6, 4, -3, -2, 3, 4, 6, 8]) == 0.6923076923076923"
    Mbpp[442]["test_list"][
        2
    ] = "assert positive_count([2, 4, -6, -9, 11, -12, 14, -5, 17]) == 0.5555555555555556"

    # Fix 461
    assert Mbpp[461]["test_list"][0] == "assert upper_ctr('PYthon') == 1"
    assert Mbpp[461]["test_list"][1] == "assert upper_ctr('BigData') == 1"
    Mbpp[461]["test_list"][0] = "assert upper_ctr('PYthon') == 2"
    Mbpp[461]["test_list"][1] = "assert upper_ctr('BigData') == 2"

    # @Soryxie Fix 83
    assert Mbpp[83]["test_list"][0] == 'assert get_Char("abc") == "f"'
    assert Mbpp[83]["test_list"][1] == 'assert get_Char("gfg") == "t"'
    assert Mbpp[83]["test_list"][2] == 'assert get_Char("ab") == "c"'
    Mbpp[83]["test_list"][0] = 'assert get_Char("abc") == chr(8)'
    Mbpp[83]["test_list"][1] = 'assert get_Char("gfg") == chr(22)'
    Mbpp[83]["test_list"][2] = 'assert get_Char("ab") == chr(13)'

    # @Soryxie Fix 115
    assert Mbpp[115]["test_list"][1] == "assert empty_dit([{1,2},{},{}])==False"
    Mbpp[115]["test_list"][1] = "assert empty_dit([{1,2},{},{}])==True"

    # @Soryxie Fix 117
    assert (
        Mbpp[117]["test_list"][0]
        == 'assert list_to_float( [("3", "4"), ("1", "26.45"), ("7.32", "8"), ("4", "8")] ) == [(3.0, 4.0), (1.0, 26.45), (7.32, 8.0), (4.0, 8.0)]'
    )
    assert (
        Mbpp[117]["test_list"][1]
        == 'assert list_to_float( [("4", "4"), ("2", "27"), ("4.12", "9"), ("7", "11")] ) == [(4.0, 4.0), (2.0, 27.0), (4.12, 9.0), (7.0, 11.0)]'
    )
    assert (
        Mbpp[117]["test_list"][2]
        == 'assert list_to_float( [("6", "78"), ("5", "26.45"), ("1.33", "4"), ("82", "13")] ) == [(6.0, 78.0), (5.0, 26.45), (1.33, 4.0), (82.0, 13.0)]'
    )
    Mbpp[117]["test_list"][
        0
    ] = 'assert list_to_float( [("3", "4"), ("1", "26.45"), ("7.32", "8"), ("4", "8")] ) == [[3.0, 4.0], [1.0, 26.45], [7.32, 8.0], [4.0, 8.0]]'
    Mbpp[117]["test_list"][
        1
    ] = 'assert list_to_float( [("4", "4"), ("2", "27"), ("4.12", "9"), ("7", "11")] ) == [[4.0, 4.0], [2.0, 27.0], [4.12, 9.0], [7.0, 11.0]]'
    Mbpp[117]["test_list"][
        2
    ] = 'assert list_to_float( [("6", "78"), ("5", "26.45"), ("1.33", "4"), ("82", "13")] ) == [[6.0, 78.0], [5.0, 26.45], [1.33, 4.0], [82.0, 13.0]]'

    # @Soryxie Fix 249
    assert (
        Mbpp[249]["test_list"][0]
        == "assert intersection_array([1, 2, 3, 5, 7, 8, 9, 10],[1, 2, 4, 8, 9])==[1, 2, 8, 9]"
    )
    assert (
        Mbpp[249]["test_list"][1]
        == "assert intersection_array([1, 2, 3, 5, 7, 8, 9, 10],[3,5,7,9])==[3,5,7,9]"
    )
    assert (
        Mbpp[249]["test_list"][2]
        == "assert intersection_array([1, 2, 3, 5, 7, 8, 9, 10],[10,20,30,40])==[10]"
    )
    Mbpp[249]["test_list"][
        0
    ] = "assert intersection_array([1, 2, 3, 5, 7, 8, 9, 10],[1, 2, 4, 8, 9])==[8, 1, 2, 9]"
    Mbpp[249]["test_list"][
        1
    ] = "assert intersection_array([1, 2, 3, 5, 7, 8, 9, 10],[3,5,7,9])==[9, 3, 5, 7]"
    Mbpp[249]["test_list"][
        2
    ] = "assert intersection_array([1, 2, 3, 5, 7, 8, 9, 10],[10,20,30,40])==[10]"

    # @Soryxie Fix 295
    assert Mbpp[295]["test_list"][0] == "assert sum_div(8)==7"
    assert Mbpp[295]["test_list"][1] == "assert sum_div(12)==16"
    assert Mbpp[295]["test_list"][2] == "assert sum_div(7)==1"
    Mbpp[295]["test_list"][0] = "assert sum_div(8)==15.0"
    Mbpp[295]["test_list"][1] = "assert sum_div(12)==28.0"
    Mbpp[295]["test_list"][2] = "assert sum_div(7)==8.0"

    # @Soryxie Fix 396
    assert Mbpp[396]["test_list"][0] == 'assert check_char("abba") == "Valid"'
    assert Mbpp[396]["test_list"][1] == 'assert check_char("a") == "Valid"'
    assert Mbpp[396]["test_list"][2] == 'assert check_char("abcd") == "Invalid"'
    Mbpp[396]["test_list"][0] = 'assert check_char("abba") == True'
    Mbpp[396]["test_list"][1] = 'assert check_char("a") == True'
    Mbpp[396]["test_list"][2] = 'assert check_char("abcd") == False'

    # @Soryxie Fix 400
    assert (
        Mbpp[400]["test_list"][0]
        == "assert extract_freq([(3, 4), (1, 2), (4, 3), (5, 6)] ) == 3"
    )
    Mbpp[400]["test_list"][
        0
    ] = "assert extract_freq([(3, 4), (1, 2), (4, 3), (5, 6)] ) == 4"

    # @Soryxie Fix 574
    assert Mbpp[574]["test_list"][0] == "assert surfacearea_cylinder(10,5)==942.45"
    assert (
        Mbpp[574]["test_list"][1]
        == "assert surfacearea_cylinder(4,5)==226.18800000000002"
    )
    assert Mbpp[574]["test_list"][2] == "assert surfacearea_cylinder(4,10)==351.848"
    Mbpp[574]["test_list"][0] = "assert surfacearea_cylinder(10,5)==942.4777960769379"
    Mbpp[574]["test_list"][1] = "assert surfacearea_cylinder(4,5)==226.1946710584651"
    Mbpp[574]["test_list"][2] = "assert surfacearea_cylinder(4,10)==351.85837720205683"

    # @Soryxie Fix 582
    assert Mbpp[582]["test_list"][0] == "assert my_dict({10})==False"
    assert Mbpp[582]["test_list"][1] == "assert my_dict({11})==False"
    Mbpp[582]["test_list"][0] = 'assert my_dict({10:""})==False'
    Mbpp[582]["test_list"][1] = 'assert my_dict({11:""})==False'

    # @Soryxie Fix 595
    assert (
        Mbpp[595]["test_list"][1] == 'assert min_Swaps("111","000") == "Not Possible"'
    )
    assert (
        Mbpp[595]["test_list"][2] == 'assert min_Swaps("111","110") == "Not Possible"'
    )
    Mbpp[595]["test_list"][1] = 'assert min_Swaps("111","000") == None'
    Mbpp[595]["test_list"][2] = 'assert min_Swaps("111","110") == None'

    # @Soryxie Fix 640
    assert (
        Mbpp[640]["test_list"][0]
        == 'assert remove_parenthesis(["python (chrome)"])==("python")'
    )
    assert (
        Mbpp[640]["test_list"][1]
        == 'assert remove_parenthesis(["string(.abc)"])==("string")'
    )
    assert (
        Mbpp[640]["test_list"][2]
        == 'assert remove_parenthesis(["alpha(num)"])==("alpha")'
    )
    Mbpp[640]["test_list"][
        0
    ] = 'assert remove_parenthesis("python (chrome)")==("python ")'
    Mbpp[640]["test_list"][1] = 'assert remove_parenthesis("string(.abc)")==("string")'
    Mbpp[640]["test_list"][2] = 'assert remove_parenthesis("alpha(num)")==("alpha")'

    # @Soryxie Fix 746
    assert Mbpp[746]["test_list"][2] == "assert sector_area(9,361)==None"
    Mbpp[746]["test_list"][2] = "assert sector_area(9,361)==255.17586328783094"

    # @Soryxie Fix 783
    assert (
        Mbpp[783]["test_list"][2]
        == "assert rgb_to_hsv(10, 215, 110)==(149.26829268292684, 95.34883720930233, 84.31372549019608)"
    )
    Mbpp[783]["test_list"][
        2
    ] = "assert rgb_to_hsv(10, 215, 110)==(149.2682926829268, 95.34883720930233, 84.31372549019608)"

    with open(fixed_path, "w") as f:
        for key in Mbpp:
            f.write(json.dumps(Mbpp[key]) + "\n")


def check_assertion_work():
    Mbpp = {}
    with open(fixed_path, "r") as f:
        for line in f:
            data = json.loads(line)
            Mbpp[data["task_id"]] = data

    for task_id, task in Mbpp.items():
        test_code = (
            task["code"]
            + "\n"
            + "\n".join(task["test_imports"])
            + "\n"
            + "\n".join(task["test_list"])
        )
        try:
            global_vars = {}
            exec(test_code, global_vars)
        except Exception as e:
            print(f"Error in task {task_id}: {e}")
            print('"""\n' + task["prompt"] + '\n"""\n')
            print(test_code)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    change_dataset()
    if args.check:
        check_assertion_work()
