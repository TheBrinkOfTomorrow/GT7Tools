import matplotlib.pyplot as plt
import numpy as np
import time

# use ggplot style for more sophisticated visuals
plt.style.use('ggplot')

def livePlotter(x_vec,y1_data,line1,identifier='',pause_time=0.1):
    if line1==[]:
        # this is the call to matplotlib that allows dynamic plotting
        plt.ion()
        fig = plt.figure(figsize=(13,6))
        ax = fig.add_subplot(111)
        # create a variable for the line so we can later update it
        line1, = ax.plot(x_vec,y1_data,'-o',alpha=0.8)        
        #update plot label/title
        plt.ylabel('Y Label')
        plt.title('Title: {}'.format(identifier))
        plt.show()
    
    # after the figure, axis, and line are created, we only need to update the y-data
    line1.set_ydata(y1_data)
    # adjust limits if new data goes beyond bounds
    if np.min(y1_data)<=line1.axes.get_ylim()[0] or np.max(y1_data)>=line1.axes.get_ylim()[1]:
        plt.ylim([np.min(y1_data)-np.std(y1_data),np.max(y1_data)+np.std(y1_data)])
    # this pauses the data so the figure/axis can catch up - the amount of pause can be altered above
    plt.pause(pause_time)
    
    # return line so we can update it again in the next iteration
    return line1

def testLivePlotter():
    size = 100
    x_vec = np.linspace(0,1,size+1)[0:-1]
    y_vec = np.random.randn(len(x_vec))
    line1 = []
    while True:
        rand_val = np.random.randn(1)
        y_vec[-1] = rand_val
        line1 = livePlotter(x_vec,y_vec,line1)
        y_vec = np.append(y_vec[1:],0.0)

def GT7Plotter(x_vec,y_vec,identifier=''):

    # Function to plot
    plt.plot(x_vec, y_vec)

    plt.ylabel('X Label')
    plt.ylabel('Y Label')
    plt.title('Title: {}'.format(identifier))
    # function to show the plot
    plt.show()

def GT7StaticMultiPlotter(x_vec, yList, nameList, identifier=''):
    if len(yList) == 0:
        return

    fig, ax = plt.subplots() 
    fig.subplots_adjust(right=0.75)

    plt.title('Title: {}'.format(identifier))
    ax.set_xlabel('Ticks') 
    ax.set_ylabel('Throttle and Brake(%)', color = 'red') 
    ax.tick_params(axis ='y', labelcolor = 'red') 
  
    # Adding Twin Axes
    twin1 = ax.twinx()      # speed (KPH)
    twin2 = ax.twinx()      # RPM
    # Offset the right spine of twin2.  The ticks and label have already been
    # placed on the right by twinx above.
    twin2.spines.right.set_position(("axes", 1.1))
    
    twin1.set_ylabel('Speed (KPH)', color = 'black') 
    twin1.tick_params(axis ='y', labelcolor = 'black') 
    twin2.set_ylabel('RPM', color = 'blue') 
    twin2.tick_params(axis ='y', labelcolor = 'blue') 

    ax.plot(x_vec, yList[0], label = 'Throttle %', color='green', linewidth=1.0)
    ax.plot(x_vec, yList[1], label = 'Brake %', color='red', linewidth=1.0, linestyle='--')
    twin1.plot(x_vec, yList[2], label = 'Speed (KPH)', color='black', linewidth=1.0)
    twin2.plot(x_vec, yList[3], label = 'RPM', color='blue', linewidth=1.0, linestyle='--')

    # function to show the plot
    plt.show()


def testGT7Plotter():
    # x-axis values
    x = [5, 2, 9, 4, 7]
    # Y-axis values
    y = [10, 5, 8, 4, 2]

    GT7DataPlotter(x, y, 'Testing...')

def main():
#    testLivePlotter()
    testGT7Plotter()
    time.sleep(20)

if __name__ == "__main__":
    main()
