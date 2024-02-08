from CGVReservationManager import CGVReservationManager
import time


def main():
    cgv = CGVReservationManager()
    cgv.get_movie_list()
    cgv.get_movie_type()
    cgv.get_region()
    cgv.get_theater()
    cgv.get_date()
    cgv.get_time()
    time.sleep(5000)


if __name__ == '__main__':
    main()
