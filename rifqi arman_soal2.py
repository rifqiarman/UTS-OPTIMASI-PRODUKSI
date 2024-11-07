from sympy import Symbol, diff, sin, cos, E, N
import matplotlib.pyplot as plt

# Fungsi untuk menghitung nilai fungsi CL(AR) pada AR
def func(expr, AR):
    # Periksa jika AR mendekati nol untuk menghindari ZeroDivisionError
    if AR == 0 or abs(AR) < 1e-6:
        return float('inf')  # Return inf untuk menghindari pembagian nol
    try:
        result = eval(expr, {'AR': AR, 'sin': sin, 'cos': cos, 'e': E})
        return round(result, 4)
    except ZeroDivisionError:
        return float('inf')  # Jika ada ZeroDivisionError kembalikan infinity

# Fungsi untuk menghitung nilai turunan fungsi CL(AR) pada AR
def deriv(expr, point):
    AR = Symbol('AR')
    fx = eval(expr, {'AR': AR, 'sin': sin, 'cos': cos, 'e': E})
    fxDash = fx.diff(AR)  # Turunan fungsi
    val = N(fxDash.subs(AR, point), 40)
    return round(val, 4)

# Algoritma Newton-Raphson untuk menemukan akar (atau maksimum dalam hal ini)
def newtonEq(input_expr, initial_point):
    f_val = func(input_expr, initial_point)
    d_val = deriv(input_expr, initial_point)
    
    # Hindari pembagian dengan nol atau angka sangat kecil
    if abs(d_val) < 1e-6:
        raise ValueError("Turunan terlalu kecil, tidak bisa melanjutkan perhitungan.")
    
    second_point = initial_point - (f_val / d_val)
    return round(second_point, 4)

# Plotting grafik fungsi dan turunan
def plotGraph(x, y, dx, dy):
    fig = plt.figure('Newton Graph')
    plt.ylabel('F(AR)')
    plt.xlabel('AR')
    plt.plot(x, y, label='F(AR)')
    plt.grid(True)

    # Plotting the d(x) tangent
    for i in range(len(dx)):
        plt.plot(dx[i], dy[i], '--', color="red")

    plt.legend(["F(AR)", "F'(AR)"], loc='upper left')

    # Save plot for debugging
    plt.savefig('newton_plot.png')
    
    # Show the plot
    plt.show()

# Plotting tabel hasil iterasi
def plotTable(tableData):
    fig = plt.figure('Newton Table')
    table = plt.table(cellText=tableData,
                      loc='center',
                      colLabels=["Iteration (I)", "ARi", "F(ARi)", "F'(ARi)", "ARi+1", "Error"],
                      colColours=["skyblue"] * 10)
    table.set_fontsize(14)
    table.scale(1, 2)
    plt.axis('off')

    # Save table plot for debugging
    plt.savefig('newton_table.png')
    
    # Show the table
    plt.show()

# Fungsi untuk memulai metode Newton-Raphson
def start(input_expr, initial_point, iterations, errorGiven, tableD, graphD):
    try:
        initial_point = float(initial_point)
    except:
        print("Starting point must be a number!")
        return

    if not iterations:
        iterations = 13

    try:
        iterations = int(iterations)
    except:
        print("Iterations must be a real number!")
        return

    if not errorGiven:
        errorGiven = 0

    try:
        errorGiven = float(errorGiven)
    except:
        print("Error must be a number!")
        return

    plt.close('all')

    # Inisialisasi ekspresi matematis untuk f(AR)
    AR = Symbol('AR')  # Definisi simbol 'AR'
    fx = eval(input_expr, {'AR': AR, 'sin': sin, 'cos': cos, 'e': E})  # Fungsi
    fxDash = diff(fx, AR)  # Turunan f(AR)

    if fxDash == 0:
        print("Can't proceed with Newton Method with a constant function 'inflection point'")
        return

    tempFirst = initial_point
    table_data = []  # Inisialisasi data tabel
    funcY = []  # Nilai y dari fungsi f(AR)
    funcX = []  # Nilai x dari fungsi f(AR)
    dfuncY = []  # Nilai turunan dari fungsi
    dfuncX = []  # Nilai x untuk turunan fungsi

    # Iterasi metode Newton-Raphson
    for i in range(iterations):
        first_point = initial_point
        try:
            initial_point = round(newtonEq(input_expr, first_point), 4)
        except ValueError as e:
            print(e)
            break
        dfuncY.append([func(input_expr, first_point), 0])
        dfuncX.append([first_point, initial_point])
        errorIt = abs(round(initial_point - first_point, 4))

        # Menambahkan data ke tabel
        table_data.append([i + 1, "%.4f" % first_point,
                           "%.4f" % func(input_expr, first_point),
                           "%.4f" % deriv(input_expr, first_point),
                           "%.4f" % initial_point,
                           "%.4f" % abs(errorIt)
                           ])
        if errorIt <= errorGiven:
            break

    last_point = int(initial_point)
    steps = abs(tempFirst - last_point) + 4

    for i in range(int(steps) * 2):
        funcY.append(func(input_expr, (last_point - 2) + (i / 2)))  # Untuk memperhalus kurva
        funcX.append((last_point - 2) + (i / 2))

    # Plot dan tabel
    if tableD:
        plotTable(table_data)

    if graphD:
        plotGraph(funcX, funcY, dfuncX, dfuncY)

    if not graphD and not tableD:
        print("You should select an output type!")

# Menjalankan metode Newton-Raphson dengan ekspresi yang diberikan dalam soal
expr = "(2 * 3.1415 * AR) / (1 + 2 / AR)"
start(expr, 5, 10, 0.001, True, True)  # Inisialisasi sesuai soal
