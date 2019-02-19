import yape
import cProfile


def main():
    yape.yape2()


def main_profile():
    cProfile.run(
        "import yape; yape.yape2()", "/Users/kazamatzuri/work/yape-testdata/stats"
    )
