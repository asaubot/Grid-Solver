import numpy as np
import string
from lxml import html
import requests


class Ruzzle :
    def __init__(self) :
        
        #######################################
        ############# BUILD GRID ############## Letters Frequency are crawled from wikipedia
        #######################################
        
        letters_f = requests.get('https://en.wikipedia.org/wiki/Letter_frequency')
        tree = html.fromstring(letters_f.content)
        letters = tree.xpath('//table[@class="wikitable sortable floatright"][1]/tbody/tr//td[@align="center"]/b/text()')
        frequency = [float(e.strip().replace('%',''))/100 for e in tree.xpath('//table[@class="wikitable sortable floatright"][1]/tbody/tr/td[@align="right"]/text()')]
        frequency = [e/sum(frequency) for e in frequency]

        self.grid = np.random.choice(letters , size = (4,4), p = frequency)

        #######################################
        ####### BUILD DICTIONARY-TRIE ########
        ####################################### 

        f = open('engmix.txt','r')
        lines = f.readline()

        dictionary = []
        while lines :
            dictionary.append(lines.strip())
            try : 
                lines = f.readline()
            except : 
                continue

        self.dictionary = self.build_trie(*dictionary)
        
    def build_trie(self,*words):
        """Build a trie structure given a list of words

        Returns:
            dict -- trie like dictionary
        """
        root = dict()
        for word in words:
            current_dict = root
            for letter in word:
                current_dict = current_dict.setdefault(letter, {})
            current_dict['_end_'] = '_end_'
        return root

    def isin_trie(self,word):
        """Check if word is present in trie

        Arguments:
            word {str} -- word to check
        Returns:
            boolean -- 
        """
        current_dict = self.dictionary
        for letter in word:
            if letter not in current_dict:
                return False
            current_dict = current_dict[letter]
        return '_end_' in current_dict

    def is_feasible(self,chars):
        """Check if starting chars could lead to a word in dictionary

        Arguments:
            chars {str} -- potential prefix of a word

        Returns:
            boolean --
        """
        current_dict = self.dictionary
        for letter in chars : 
            if letter not in current_dict:
                return False
            current_dict = current_dict[letter]
        return True

    def neighborhood(self,pos):
        """ Given a position on the grid , return all neighbors of the current position (1 radius)

        Arguments:
            pos {tuple} -- position on the grid

        Yields:
            tuple -- next neighbor
        """
        for i in range(pos[0] - 1 , pos[0] + 2) :
            for j in range(pos[1] - 1 , pos[1] + 2) :
                if (0 <= i < self.grid.shape[0] and 0 <= j < self.grid.shape[1]) and (i != pos[0] or j != pos[1]): 
                    yield (i,j)

    def DFS(self,pos,visited = [] , words = []) :
        """Implementation of depth first search with backtracking to test if current state could lead to a word in dictionary

        Arguments:
            pos {tuple} -- initial position on grid (first letter)

        Keyword Arguments:
            visited {list} -- visited letters at the current state of DFS (default: {[]})
            words {list} -- list of word found during DFS (default: {[]})

        Returns:
            list -- all words found from pos
        """
        visited.append(pos)
        w = ''.join([self.grid[e] for e in visited])
        words += [w] if self.isin_trie(w) else []
        
        for neighbor in self.neighborhood(pos) : 
            if neighbor not in visited and self.is_feasible(w+self.grid[neighbor]):
                self.DFS(neighbor,visited.copy(),words)

        return words

    def find_all(self) :
        """Perform a DFS from all position in the grid

        Returns:
            list  -- all words found in the grid
        """
        ws = []
        for i, j in np.ndindex(self.grid.shape) :
            candidates = self.DFS(pos = (i,j),visited = [] ,words = [])
            ws += candidates if len(candidates) else []
        return sorted(list(set([e for e in ws if len(e) > 1])), key=len)

    def __str__(self):
        s = '\n'
        for i in range(self.grid.shape[0]):
            for j in range(self.grid.shape[1]):
                s += self.grid[i,j].upper() + '  '
            s += '\n'
        return s

    def __repr__(self):
        return self.__str__()



R = Ruzzle()
R
print(R.find_all())