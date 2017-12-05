class FilterParameter():
    def __init__(self, columnName, operation ,columnValue, linkOperation = "AND "):
        self.columnName = columnName
        self.columnValue = columnValue
        self.operation = operation
        self.linkOperation = linkOperation