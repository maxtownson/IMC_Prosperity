import random
import plotly.graph_objs as go

def pdf(x):
    return (1/5000 * x) - 9/50

def cdf(x):
    return (1/10000 * (x ** 2)) - (9/50 * x) + 81

def profit(p1, p2):
    return ((cdf(p1))) * (1000 - p1) + ((cdf(p2) - cdf(p1)) * (1000 - p2))

def generateRandomNums():
    p1_prelim = random.randint(901, 1000)
    p2_prelim = random.randint(901, 1000)

    p2 = max(p1_prelim, p2_prelim)
    p1 = min(p1_prelim, p2_prelim)

    return p1, p2

def main():

    print(profit(950, 960))

    p1_values = []
    p2_values = []
    profit_values = []
    for i in range(100000):
        p1, p2 = generateRandomNums()
        while p1 == p2:
            p1, p2 = generateRandomNums()

        prof = profit(p1, p2)
        p1_values.append(p1)
        p2_values.append(p2)
        profit_values.append(prof)

    # Create a 3D scatter plot
    fig = go.Figure(data=[go.Scatter3d(
        x=p1_values,
        y=p2_values,
        z=profit_values,
        mode='markers',
        marker=dict(
            size=5,
            color=profit_values,
            colorscale='Viridis',
            opacity=0.8
        )
    )])

    fig.update_layout(scene=dict(
                    xaxis_title='p1',
                    yaxis_title='p2',
                    zaxis_title='Profit'),
                  title='Profit Distribution')
    
    fig.show()

    # Find the maximum profit and its corresponding coordinates
    max_profit_index = profit_values.index(max(profit_values))
    max_p1 = p1_values[max_profit_index]
    max_p2 = p2_values[max_profit_index]
    max_profit = profit_values[max_profit_index]

    print("Maximum Profit Coordinates:")
    print("p1 =", max_p1)
    print("p2 =", max_p2)
    print("Profit =", max_profit)

if __name__ == "__main__":
    main()