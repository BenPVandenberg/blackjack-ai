import os


def get_profits(folder):
    all_profits = []

    subfolders = os.listdir(folder)
    subfolders.sort(key=int)

    # go through all folders in the folder
    for subfolder in subfolders:
        # read profit from total_profit.txt
        with open(os.path.join(folder, subfolder, 'total_profit.txt'),
                  'r') as f:
            profit = int(f.read())

            all_profits.append(profit)

            if profit == -903300:
                print(subfolder)

    return all_profits


if __name__ == "__main__":
    print(get_profits("gen_data_round_2"))
