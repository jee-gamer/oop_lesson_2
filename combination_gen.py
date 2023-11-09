def gen_comb_list(list_set):
    '''
        Parameters:
            list_set: a list of lists where each contains at least one element

        Returns:
            a list of lists, each of which is made from a combination of elements in each list in list_set

        Examples:
            gen_comb_list([[1, 2, 3]]) returns [[1], [2], [3]]
            gen_comb_list([[1, 2, 3], [4, 5]]) returns [[1, 4], [2, 4], [3, 4], [1, 5], [2, 5], [3, 5]]
            gen_comb_list([[1, 2, 3], [4, 5], [6, 7, 8]]) returns [[1, 4, 6], [2, 4, 6], [3, 4, 6], [1, 5, 6], [2, 5, 6], [3, 5, 6], [1, 4, 7], [2, 4, 7], [3, 4, 7], [1, 5, 7], [2, 5, 7], [3, 5, 7], [1, 4, 8], [2, 4, 8], [3, 4, 8], [1, 5, 8], [2, 5, 8], [3, 5, 8]]
    '''

    if not list_set:
        return [[]]

    def combine_lists(list1, list2):  # combine 2 list combination
        """
        run through for loop for each list then
        make a combined list for each item [1,2] (concatenates)
        then append that to result
        """
        result = []
        for item1 in list1:
            for item2 in list2:
                result.append(item1 + [item2])
        return result

    result = [[]]
    for sublist in list_set:  # big list + small list
        """
        for example [1,2],[2,3] + [4,5]
        so it goes
        [1,2,4],[1,2,5],[2,3,4],[2,3,5]
        """
        result = combine_lists(result, sublist)
    return result


print(gen_comb_list([[1, 2, 3], [4, 5]]))
