from elifozer_utilities.filterparameter import FilterParameter


class FilterExpression(FilterParameter):
    def __init__(self):
        self.parameters = []


    def AddParameter(self, parameter):
        self.parameters.append(parameter)


    def GetWhere(self):
        if len(self.parameters) == 0:
            return ""

        whereCondition = " WHERE "
        counter = len(self.parameters)
        i = 0

        while i < counter:
            whereCondition += self.parameters[i].columnName + " " + self.parameters[i].operation + " %s "

            if i+1 < counter:
                whereCondition += self.parameters[i].linkOperation

            i +=1

        return whereCondition


    def GetParameters(self):
        tempParameters = []

        if len(self.parameters) == 0:
            return tempParameters

        for i in self.parameters:
            tempParameters.append(i.columnValue)

        return tuple(tempParameters)