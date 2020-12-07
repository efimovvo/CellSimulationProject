'''This module will contain functions for reading from file and
for writing to file'''


def write_data(list_cells, time):
    """ Function add line in data.txt file

    Parameters
    ----------
    list_cells : list
        list of cells
    time : int
        current time = step of modelling

    Returns
    ----------
    """
    list_victim = [cell for cell in list_cells if not cell.predator]
    list_predator = [cell for cell in list_cells if cell.predator]
    if list_victim != 0:
        with open('data.txt', 'a') as file:
            cell_data = [str(len(list_victim)), str(len(list_predator)), str(time)]
            cell_data = ' '.join(cell_data)
            cell_data = cell_data + '\n'
            file.write(cell_data)


def read_data():
    """ Function reads data from data.txt file

        Parameters
        ----------

        Returns
        ----------
        victims_list : list
            list of victim population at the moments in time
        predators_list : list
            list of predator population at the moments in time
        time : list
            list of time moments
        """
    input_data = []
    victims_list = []
    predators_list = []
    time = []
    with open('data.txt', 'r') as file:
        for line in file:
            input_data.append(line.split())
    for i in range(len(input_data)):
        victims_list.append(int(input_data[i][0]))
        predators_list.append(int(input_data[i][1]))
        time.append(int(input_data[i][2]))

    return victims_list, predators_list, time
