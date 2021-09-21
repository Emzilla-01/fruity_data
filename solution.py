#!/usr/bin/env python3
"""
6-16-2021
Emy Kay's submission to Corey Fink's AAE Programming Exercise

This module provides a FruitBasket class as a solution, with various methods associated with each requirement.

There is some ambiguity in the problem statement, so some requirements have multiple associated methods or single methods with different relevant args.

Updates can be made to improve optimization, readability, code organization per request. The idea is to present a fully featured first cut per the requirements.

8-23-2021 : `how to write good code comments`??? 🤔🤔🤔
9-20-2021 : reviewing this because I thirst for coding but didn't code today at work... Add TODO on sys.argv, 
"""

import sys
import os
from pprint import pprint
#print(sys.argv[1]) # only uses sys.argv[1] as expected .csv inputs - no other args

class FruitBasket():
    def text_formatter(self, s):
        for c in r"'()[]":
            s = s.replace(c, "")
        return(s)

    def __init__(self, data_path=sys.argv[1]): # mistake: sys.argv[1] should be called in main(), not in init. If we call multiple [FruitBasket() for fb in path_list], this would break. If this is imported into another script which takes its own sys.argv, this would break.
        self.fruitdict = dict()
        with open(os.path.abspath(sys.argv[1]), 'rt') as fruitdata:
            i=0
            for line in fruitdata.readlines():
                r_ = line.replace("\n","").split(',')
                if i == 0: 
                    colnames = list(enumerate(r_)) #Expects header!
                else:
                    self.fruitdict[i]=dict()
                    self.fruitdict[i]['chars']=list()
                    for ix, key in colnames:
                        if "characteristic" not in key:
                            self.fruitdict[i][key] = r_[ix]
                        else:
                            self.fruitdict[i]['chars'].append(r_[ix].strip())
                            self.fruitdict[i]['chars'] = sorted(self.fruitdict[i]['chars']) # Ensuring consistent order in cases where data may be unordered...
                i+=1
        #pprint(self.fruitdict)
        
    def get_total_items_in_inventory(self):
        """requirement #1: 'Total number of fruit'
        This method interprets the requirement to mean 'Total items in fruit inventory'. This would be the same as rows (excluding header) in the input data.
        """
        a = len(self.fruitdict)
        #print(f"We have {a} fruit items in inventory")
        return(a)
    
    def get_fruit_types(self, verbose=False):
        """ requirement #2: 'Total types of fruit'
        This method interprets this requirement to mean each type of fruit per name and attributes.
        
        So if we have 2x red sweet apple,
                      1x yellow sweet apple,
                      1x green tart apple,
                      
        This method would say we have 3 types of fruit.
        """
       
        self.fruit_types_set = {(v['fruit'], tuple(v['chars'])) for v in self.fruitdict.values()}
       
        if verbose:
            print("Each type of fruit:\n")
            for val in self.fruit_types_set:
                s = f"{val[1]} {val[0]}"
                s = self.text_formatter(s)
                print(s)
            print()
        self.types_of_fruit_sum = len(self.fruit_types_set)
        
        return(self.types_of_fruit_sum)
    
    def get_fruit_naive(self, verbose=False):
        """ requirement #2: 'Total types of fruit'
        This method interprets requirement #2 to mean that each type of fruit is the same regardless of characteristics.
        
        So if we have 2x red sweet apple,
                      1x yellow sweet apple,
                      1x green tart apple,
                      
        This method would say we have only 1 type of fruit ('apple').
        """
        try:
            self.fruit_types_set
        except AttributeError as e:
            self.fruit_types_set = {(v['fruit'], tuple(v['chars'])) for v in self.fruitdict.values()}
        self.fruit_types_naive = {v['fruit'] for v in self.fruitdict.values()}
        self.fruit_types_naive_sum = len(self.fruit_types_naive)
        if verbose:
            print("Each type of fruit:")
            print("\n".join(self.fruit_types_naive ))
            print()
        return(self.fruit_types_naive_sum )    

    def count_fruit(self, naive=True):
        """Requirement #3: 'The number of each type of fruit in descending order"""
        try:
            self.fruit_types_naive
        except AttributeError as e:
            _ = self.get_fruit_naive()
        self.fruit_counts = list()
        for f_t in self.fruit_types_naive:
            count = len([v['fruit'] for v in self.fruitdict.values() if v['fruit']==f_t])
            self.fruit_counts.append([f_t, count])
                    
        self.fruit_counts.sort(key=lambda r: r[1], reverse=True)
        print("The number of each type of fruit in descending order:")
        [print(f"{v[0]} : {v[1]}") for v in self.fruit_counts]
        

    def get_fruit_characteristics(self, flat=False):
        """Requirement 4: The characteristics (size, color, shape, etc.) of each fruit by type
       
       If flat=False, considers type as each unique combination of (fruit, *attrs).
               So if we have 
                      2x red sweet apple,
                      1x yellow sweet apple,
                      1x green tart apple,
            
            method will return:
                      1 apple : sweet, yellow
                      1 apple : green, tart
                      2 apple : red, sweet
                    
       If flat=True, considers type as (fruit), and lists all attrs associated with that fruit
            
            4 apples, green, red, sweet, tart, yellow
    """
        try:
            self.fruit_types_naive
        except AttributeError as e:
            _ = self.get_fruit_naive()
        
        self.fruit_chars_counts_dict = dict()
        if not flat:
            for fruit_type in self.fruit_types_set:
                self.fruit_chars_counts_dict[fruit_type] = len(
                [v for v in self.fruitdict.values() if v['fruit']==fruit_type[0] and v['chars']==list(fruit_type[1])]
                )
            print("\nThe characteristics (size, color, shape, etc.) of each fruit by type (treating unique fruits as tuple of attrs):")
                        
            [print(self.text_formatter(f"{itm[1]} {itm[0][0]}s : {itm[0][1]} ")) for itm in self.fruit_chars_counts_dict.items()] # TODO assign a name instead of writing out a long comprehension twice.
            return([self.text_formatter(f"{itm[1]} {itm[0][0]} : {itm[0][1]} ") for itm in self.fruit_chars_counts_dict.items()])
        else:
            try:
                counts_dict = dict(self.fruit_counts)
            except AttributeError as e:
                _ = self.count_fruit()
                counts_dict = dict(self.fruit_counts)
                
            for fruit_type in self.fruit_types_set:
                self.fruit_chars_counts_dict.setdefault(fruit_type[0],{'count':0, 'attrs':list()})
                [self.fruit_chars_counts_dict[fruit_type[0]]['attrs'].append(attr) for attr in fruit_type[1]]
                self.fruit_chars_counts_dict[fruit_type[0]]['attrs'] = sorted(list(set(self.fruit_chars_counts_dict[fruit_type[0]]['attrs']))) # TODO: would self.dict_[k][a].sort() work?
                self.fruit_chars_counts_dict[fruit_type[0]]['count'] = counts_dict[fruit_type[0]]
            
            print("\nThe characteristics (size, color, shape, etc.) of each fruit by type (flat/naive):")            
            [print(self.text_formatter(f"{itm[1]['count']} {itm[0]}s : {', '.join(itm[1]['attrs'])}")) for itm in self.fruit_chars_counts_dict.items()]
                        
    def plural_formatter(self, itm):
        if itm[1] > 1:
            s = f"{itm[1]} {itm[0]}s"
        if itm[1] == 1:
            s = f"{itm[1]} {itm[0]}"
        return(s)
        
    def get_stale(self, limit = 3):
        """Returns items older than the limit arg using naive fruit type ('apple', 'orange')        
           Sets FruitBasket.stale_item_ixs to indicate indices of each stale item so fruit can be taken off the shelf.
        """
        print("\nHave any fruit been in the basket for over 3 days")
        stale_items_dict = {k:v for k,v in self.fruitdict.items() if int(v['days'])>limit}
        self.stale_item_ixs = [k+1 for k in stale_items_dict.keys()] # k+1 will match Excel indexing to identify stale items
        stale_items_vals = {f: len([v for v in stale_items_dict.values() if v['fruit']==f]) for f in self.fruit_types_naive}
        stale_items_vals = {k: v for k,v in stale_items_vals.items() if v>0}
        if len(stale_items_vals) == 0:
            stale_items_str = "No items older than {limit} days old."
        elif len(stale_items_vals) == 1:
            stale_items_str = f"{self.plural_formatter(list(stale_items_vals.items())[0])} is over {limit} days old"
        elif len(stale_items_vals) == 2:
            stale_items_str = " and ".join([self.plural_formatter(itm) for itm in stale_items_vals.items()]) + f" are over {limit} days old"
        
        elif len(stale_items_vals) > 2:
            stale_items_str = ", ".join([self.plural_formatter(itm) for itm in list(stale_items_vals.items())[:-1]]) \
            + " and " \
            + self.plural_formatter(tuple(list(stale_items_vals.items())[-1]))  + f" are over {limit} days old"
        else:
            raise Exception("Problem in days column")
        print(stale_items_str)
    
######################
# main
######################

def main(): #TODO - use sys.argv in main() instead of in FruitBasket.__init__...
    basket = FruitBasket() 
    print(f"Total number of fruit: {basket.get_total_items_in_inventory()}\n")  
    basket.count_fruit()
    basket.get_fruit_characteristics(flat=False)
    basket.get_fruit_characteristics(flat=True)
    basket.get_stale()
    
if __name__ == "__main__":
    main()
