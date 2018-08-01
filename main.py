from Pool import Pool
import sys


def main():
    if len(sys.argv) <= 1:
        print("Please provide more arguments")
        return

    pool = Pool()

    while True:
        score = pool.execute_trees()
        print(score)
        #for tree in pool.trees:
            #print(tree.lines())

        write_file(pool.best_tree.lines())
        if score == 0:
            break
        pool.alter_best_tree()

    code = pool.best_tree.lines()
    f = open(sys.argv[1], "w+")
    for line in code:
        f.write(line + "\n")
    f.close()


def write_file(lines):
    f = open(sys.argv[1], "w+")
    for line in lines:
        f.write(line + "\n")
    f.close()

main()