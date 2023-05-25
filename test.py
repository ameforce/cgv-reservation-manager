from CGVReservationManager import CGVReservationManager
import time


def main():
    cgv = CGVReservationManager()
    cgv.get_movie_list()
    time.sleep(5000)


if __name__ == '__main__':
    main()
