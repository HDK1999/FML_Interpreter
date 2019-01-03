with open('./ubuntu_logo.fml', 'w') as file:
    file.writelines('scale is (5, 5);\n')
    file.writelines('background is (0, 0, 0);\n')
    file.writelines('color is (221, 72, 20);\n')
    for i in range(33):
        file.writelines('for t from 0 to 2 * pi step pi / 1000 draw ({r} * cos(t), - {r} * sin(t));\n'.format(r=i))
    for i in range(33, 38):
        file.writelines('for t from 0 to 2 * pi step pi / 10000 draw ({r} * cos(t), - {r} * sin(t));\n'.format(r=i))
    for i in range(58, 63):
        file.writelines('for t from 0 to 2 * pi step pi / 10000 draw ({r} * cos(t), - {r} * sin(t));\n'.format(r=i))
    for i in range(63, 95):
        file.writelines('for t from 0 to 2 * pi step pi / 1000 draw ({r} * cos(t), - {r} * sin(t));\n'.format(r=i))
    for i in range(95, 101):
        file.writelines('for t from 0 to 2 * pi step pi / 10000 draw ({r} * cos(t), - {r} * sin(t));\n'.format(r=i))

    file.writelines('color is (255, 255, 255);\n')
    for i in range(38, 43):
        file.writelines('for t from 0 to 2 * pi step pi / 10000 draw ({r} * cos(t), - {r} * sin(t));\n'.format(r=i))
    for i in range(43, 52):
        file.writelines('for t from 0 to 2 * pi step pi / 1000 draw ({r} * cos(t), - {r} * sin(t));\n'.format(r=i))
    for i in range(52, 58):
        file.writelines('for t from 0 to 2 * pi step pi / 10000 draw ({r} * cos(t), - {r} * sin(t));\n'.format(r=i))

    file.writelines('color is (221, 72, 20);\n')
    for i in range(3):
        file.writelines('rot is pi * 2 * {i} / 3;\n'.format(i=i))
        file.writelines('for t from 35 to 65 step 0.1 draw (t, -2);\n')
        file.writelines('for t from 35 to 65 step 0.1 draw (t, -1);\n')
        file.writelines('for t from 35 to 65 step 0.1 draw (t, 0);\n')
        file.writelines('for t from 35 to 65 step 0.1 draw (t, 1);\n')
        file.writelines('for t from 35 to 65 step 0.1 draw (t, 2);\n')
        file.writelines('for t from 35 to 65 step 0.1 draw (t, 3);\n')

    for i in range(3):
        file.writelines('rot is pi * (2 * {i} - 1) / 3;\n'.format(i=i))
        file.writelines('color is (255, 255, 255);\n')
        for j in range(14):
            file.writelines('for t from 0 to 2 * pi step pi / 10000 draw ({r} * cos(t) + 67.5, - {r} * sin(t));\n'.format(r=j))
        file.writelines('color is (221, 72, 20);\n')
        for j in range(14, 19):
            file.writelines(
                'for t from pi / 2 to 3 * pi / 2 step pi / 10000 draw ({r} * cos(t) + 67.5, - {r} * sin(t));\n'.format(r=j))
