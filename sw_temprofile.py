'''
Calc 5-order spline from dat file

Implementation was taken from https://www.codecamp.ru/blog/curve-fitting-python/

'''

import glob
import os
import numpy as np
import matplotlib.pyplot as plt

def dat_file_write(data_list: list, out_filepath: str, header : str = None) -> None:
    '''
    Write *.dat file from data list
    '''
    write_list = []

    if header is not None:
        data_list.insert(0, header)

    for data in data_list:
        output_str = ""
        for val in data:
            output_str += str(val) + "\t"
        output_str = output_str[:-1]
        output_str += "\n"
        write_list.append(output_str)

    with open(out_filepath,"w", encoding='utf-8') as output_file:
        output_file.writelines(write_list)

def dat_file_read(in_filepath, has_header: bool = False) -> list:
    '''
    Read *.dat file to data list
    '''
    read_list= []

    lines = None
    try:
        with open(in_filepath, "r", encoding='utf-8') as input_file:
            lines = input_file.readlines()
    except UnicodeDecodeError:
        with open(in_filepath, 'r', encoding='utf-16') as input_file:
            lines = input_file.readlines()

    for idx, line in enumerate(lines):
        if has_header and idx == 0:
            continue

        line_list = []
        for val in line.split('\t'):
            line_list.append(val.replace("\n", ""))
        read_list.append(line_list)

    return read_list

def calc_spline5(data_list : list, is_need_to_show : bool = False) -> list:
    output_list = []

    # Read data from data_list dedicated list
    x = []
    y = []
    y_tp_altitude = []
    for idx, val in enumerate(data_list):
        x.append(idx)
        y.append(float(val[1]))
        y_tp_altitude.append(float(val[0]))

    model = np.poly1d(np.polyfit(x, y, 5))
    x_p = np.linspace(x[0], x[-1], len(x))
    y_p = model(x_p)

    if is_need_to_show:
        plt.scatter(x, y)
        plt.plot(x_p, y_p, color='purple')
        plt.show()

    output_list.append(['idx', 'tp_altitude', 'temp' 'temp_spline5'])
    for idx in range(x_p.size):
        output_list.append([x_p[idx], y_tp_altitude[idx], y[idx], y_p[idx]])

    return output_list

def main():
    INPUT_PATH_MASK = "./input/*.dat"
    OUTPUT_PATH = "./output"

    print("Script is started")
    print()

    files = glob.glob(INPUT_PATH_MASK)
    for filepath in files:
        print("Process >> " + filepath)

        try:
            data_list = dat_file_read(filepath, has_header=True)
            spline_list = calc_spline5(data_list)

            dat_file_write(spline_list, f"{OUTPUT_PATH}/{os.path.basename(filepath).split('.')[0]}_spline5.dat")
            print("Successful >> " + filepath)
        except Exception as exception:
            print()
            print("Cannot process >> ", filepath)
            print("Reason >> " + str(exception))
        finally:
            print()


    print("Script is finished")

if __name__ == "__main__":
    main()
