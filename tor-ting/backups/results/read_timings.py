import json
nodes = []
class Measurement:
  def __init__(self, x, y, rtt):
    self.x = x
    self.y = y
    self.rtt = rtt
  def printMeasurement(self):
    data = [self.x,self.y,self.rtt]
    return data
class Node:

    def __init__(self, fp):
        self.fp = fp
        self.rtts = []
        self.measurements = []

    def getHighestRtt(self):
        return max(self.rtts)
    def getLowestRtt(self):
        return min([x for x in self.rtts if x >= 0 ])
    def getMeasurements(self):
        measurements_list = []
        for measurement in self.measurements:
            measurements_list.append(measurement.printMeasurement())
        return measurements_list


def read_json():
    with open('2020-02-26.json', 'r') as infile:
        data = infile.readlines()
        data = [json.loads(item.replace('\n', '')) for item in data]
        return data
def sort_y(m):
    return m.y
def sort_x(m):
    return m.x
def sort_rtt(m):
    return m.rtt
def get_nodes(node_list):
    fp_list = []
    for n in node_list:
        fp_list.append(n.fp)
    return fp_list
def writeLowestTime(measurement):
    file1 = open("lowest_latencies.txt","a")
    #\n is placed to indicate EOL (End of Line)
    file1.write(str(measurement)+"\n")
    file1.close() #to change file access modes
def main():
    measurements = []
    #nodes = []
    data = read_json()
    print(len(data))
    print(len(data[0]))
    for dp in data:
        if 'rtt' in str(dp):
            new_measurement = Measurement(y=dp['y']['fp'], x=dp['x']['fp'], rtt=dp['trials'][0]['rtt'])
            measurements.append(new_measurement)
    for m in measurements:
        if m.y not in get_nodes(nodes):
            #print("y", m.rtt, m.y)
            new_node = Node(fp=m.y)
            new_node.measurements.append(m)
            #print(m.rtt, new_node.rtts)
            new_node.rtts.append(m.rtt)
            nodes.append(new_node)
        if m.x not in get_nodes(nodes):
            #print("x", m.rtt, m.x)
            new_node = Node(fp=m.x)
            new_node.measurements.append(m)
            #print(m.rtt, new_node.rtts)
            new_node.rtts.append(m.rtt)
            nodes.append(new_node)
        if m.x in get_nodes(nodes):
            for n in nodes:
                if n.fp ==  m.x:
                    n.measurements.append(new_measurement)
                    n.rtts.append(m.rtt)
        if m.y in get_nodes(nodes):
            for n in nodes:
                if n.fp ==  m.y:
                    n.measurements.append(new_measurement)
                    n.rtts.append(m.rtt)

    sorted_measurements= sorted(measurements, key=sort_rtt)
    #for m in sorted_measurements:
        #print(m.y, m.x, m.rtt)
    for n in nodes:
    	writeLowestTime(n.getLowestRtt())
        print(n.fp, n.getHighestRtt(), n.getLowestRtt(), len(n.getMeasurements()), len(n.measurements))
        #print(n.fp, "Highest RTT:", n.getHighestRtt(), "Lowest RTT:", n.getLowestRtt(), len(n.getMeasurements()), len(n.measurements))


if __name__ == "__main__":
    main()
