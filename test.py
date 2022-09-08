import numpy as np

while True:

    try:

        rand = np.random.rand()
        print(f'number: {rand}')

        if rand > 0.9:
            print('pass')
            break
        else:
            print('fail')

    except:
        pass
