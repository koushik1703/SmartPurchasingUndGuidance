class QueryConstructor:

    queryConstructor = None

    def getInstance():
        if QueryConstructor.queryConstructor == None:
            QueryConstructor.queryConstructor = QueryConstructor()
        return QueryConstructor.queryConstructor


    def constructWithOneParameter(self, component, parameterOneKey, parameterOneValue):
        query = ".//"+ component +"[@" + parameterOneKey +"='" + parameterOneValue + "']"
        return query

    def constructWithTwoParameter(self, component, parameterOneKey, parameterOneValue,  parameterTwoKey, parameterTwoValue):
        query = ".//" + component + "[@" + parameterOneKey + "='" + parameterOneValue + "'][@" + parameterTwoKey +"='" + parameterTwoValue + "']"
        return query

    def constructWithFourParameter(self, component, parameterOneKey, parameterOneValue,  parameterTwoKey, parameterTwoValue,  parameterThirdKey, parameterThirdValue,  parameterFourthKey, parameterFourthValue):
        query = ".//" + component + "[@" + parameterOneKey + "='" + parameterOneValue + "'][@" + parameterTwoKey + "='" + parameterTwoValue + "'][@" + parameterThirdKey + "='" + parameterThirdValue + "'][@" + parameterFourthKey + "='" + parameterFourthValue + "']"
        return query