from ParseTree import *

class CompilerParser :

    def __init__(self,tokens):
        """
        Constructor for the CompilerParser
        @param tokens A list of tokens to be parsed
        """
        self.tokens = tokens
        self.pos = 0
    

    def next(self):
        self.pos += 1
        return self.current()
    
    def current(self):
        return self.tokens[self.pos] if len(self.tokens) > self.pos else None
    
    def have(self, type = None, val = None):
        token = self.current();
        if not token:
            return False
        if type is not None and token.getType() not in type :
            return False
        if val is not None and token.getValue() not in val :
            return False
        return True
        
    def mustbe(self, type = None, val = None):
        if not self.have(type, val):
            raise ParseException("The token is not matches")
        token = self.current()
        self.next()
        return token
    
    def compileProgram(self):
        """
        Generates a parse tree for a single program
        @return a ParseTree that represents the program
        """
        if not self.have(['keyword'], ['class']) :
            raise ParseException("Program must begin with a class declaration")
        
        root = self.compileClass()

        return root 
    
    
    
    def compileClass(self):
        """
        Generates a parse tree for a single class
        @return a ParseTree that represents a class
        """
        node = ParseTree('class', None)
        
        kw = self.mustbe(['keyword'],['class'])
        node.addChild(ParseTree(kw.getType(), kw.getValue()))

        id = self.mustbe(['identifier'], None)
        node.addChild(ParseTree(id.getType(), id.getValue()))

        sym_o = self.mustbe(['symbol'], ['{'])
        node.addChild(ParseTree(sym_o.getType(), sym_o.getValue()))

        while True:
            if self.have(['keyword'], ['static', 'field']):
                classVar = self.compileClassVarDec()
                node.addChild(classVar)
            elif self.have(['keyword'], ['constructor', 'function', 'method']):
                subroutine = self.compileSubroutine()
                node.addChild(subroutine)
            else:
                break
        
        sym_c = self.mustbe(['symbol'], ['}'])
        node.addChild(ParseTree(sym_c.getType(), sym_c.getValue()))

        return node
    

    def compileClassVarDec(self):
        """
        Generates a parse tree for a static variable declaration or field declaration
        @return a ParseTree that represents a static variable declaration or field declaration
        """
        node = ParseTree('classVarDec', None)
        kw1 = self.mustbe(['keyword'], ['static', 'field'])
        node.addChild(ParseTree(kw1.getType(), kw1.getValue()))
        if self.have(['keyword'], ['int','char','boolean']):
            kw2 = self.mustbe(['keyword'], ['int', 'char', 'boolean'])
        else:
            kw2 = self.mustbe(['identifier'], None)
        node.addChild(ParseTree(kw2.getType(), kw2.getValue()))

        id = self.mustbe(['identifier'], None)
        node.addChild(ParseTree(id.getType(), id.getValue()))

        while self.have(['symbol'], [',']):
            sym = self.mustbe(['symbol'], [','])
            node.addChild(ParseTree(sym.getType(), sym.getValue()))
            id = self.mustbe(['identifier'], None)
            node.addChild(ParseTree(id.getType(), id.getValue()))

        sym = self.mustbe(['symbol'], [';'])
        node.addChild(ParseTree(sym.getType(), sym.getValue()))
        return node
    

    def compileSubroutine(self):
        """
        Generates a parse tree for a method, function, or constructor
        @return a ParseTree that represents the method, function, or constructor
        """
        node = ParseTree('subroutine', None)

        kw1 = self.mustbe(['keyword'], ['constructor', 'function', 'method'])
        node.addChild(ParseTree(kw1.getType(), kw1.getValue()))

        if self.have(['keyword'], ['void', 'int', 'char', 'boolean']):
            kw2 = self.mustbe(['keyword'], ['void', 'int', 'char', 'boolean'])
        else:
            kw2 = self.mustbe(['identifier'], None)
        node.addChild(ParseTree(kw2.getType(), kw2.getValue()))

        id = self.mustbe(['identifier'], None)
        node.addChild(ParseTree(id.getType(), id.getValue()))

        sym_o = self.mustbe(['symbol'], ['('])
        node.addChild(ParseTree(sym_o.getType(), sym_o.getValue()))
        
        while not self.have(['symbol'], [')']):
            parameterList = self.compileParameterList()
            node.addChild(parameterList)

        sym_c = self.mustbe(['symbol'], [')'])
        node.addChild(ParseTree(sym_c.getType(), sym_c.getValue()))

        subroutineBody = self.compileSubroutineBody()
        node.addChild(subroutineBody)

        return node
    
    
    def compileParameterList(self):
        """
        Generates a parse tree for a subroutine's parameters
        @return a ParseTree that represents a subroutine's parameters
        """
        node = ParseTree('parameterList', None)
        if self.have(['keyword'], ['int', 'char', 'boolean']):
            kw = self.mustbe(['keyword'], ['int', 'char', 'boolean'])
        else:
            kw = self.mustbe(['identifier'], None)
        node.addChild(ParseTree(kw.getType(), kw.getValue()))
        id = self.mustbe(['identifier'], None)
        node.addChild(ParseTree(id.getType(), id.getValue()))

        while self.have(['symbol'], [',']):
            sym = self.mustbe(['symbol'], [','])
            node.addChild(ParseTree(sym.getType(), sym.getValue()))

            if self.have(['keyword'], ['int', 'char', 'boolean']):
                kw = self.mustbe(['keyword'], ['int', 'char', 'boolean'])
            else:
                kw = self.mustbe(['identifier'], None)
            node.addChild(ParseTree(kw.getType(), kw.getValue()))

            id = self.mustbe(['identifier'], None)
            node.addChild(ParseTree(id.getType(), id.getValue()))
        return node
    
    
    def compileSubroutineBody(self):
        """
        Generates a parse tree for a subroutine's body
        @return a ParseTree that represents a subroutine's body
        """
        node = ParseTree('subroutineBody', None)

        sym_o = self.mustbe(['symbol'], ['{'])
        node.addChild(ParseTree(sym_o.getType(), sym_o.getValue()))

        while self.have(['keyword'], ['let', 'var']):

            if self.have(['keyword'], ['var']):
                varDec = self.compileVarDec()
                node.addChild(varDec)

            if self.have(['keyword'], ['let', 'if', 'while','do','return']):
                statement = self.compileStatements()
                node.addChild(statement)

        sym_c = self.mustbe(['symbol'], ['}'])
        node.addChild(ParseTree(sym_c.getType(), sym_c.getValue()))

        return node
    
    
    def compileVarDec(self):
        """
        Generates a parse tree for a variable declaration
        @return a ParseTree that represents a var declaration
        """
        node = ParseTree('varDec', None)

        kw1 = self.mustbe(['keyword'], ['var'])
        node.addChild(ParseTree(kw1.getType(), kw1.getValue()))
        if self.have(['keyword'], ['int', 'char', 'boolean']):
            kw2 = self.mustbe(['keyword'], ['int', 'char', 'boolean'])
        else:
            kw2 = self.mustbe(['identifier', None])
        node.addChild(ParseTree(kw2.getType(), kw2.getValue()))

        id = self.mustbe(['identifier'], None)
        node.addChild(ParseTree(id.getType(), id.getValue()))
        while self.have(['symbol'], [',']):
            sym = self.mustbe(['symbol'], [','])
            node.addChild(ParseTree(sym.getType(), sym.getValue()))
            id = self.mustbe(['identifier'], None)
            node.addChild(ParseTree(id.getType(), id.getValue()))
        sym = self.mustbe(['symbol'], [';'])
        node.addChild(ParseTree(sym.getType(), sym.getValue()))
        
        return node
    

    def compileStatements(self):
        """
        Generates a parse tree for a series of statements
        @return a ParseTree that represents the series of statements
        """
        node = ParseTree('statements', None)

        while True:
            if self.have(['keyword'], ['let']):
                letStatement = self.compileLet()
                node.addChild(letStatement)
            elif self.have(['keyword'], ['if']):
                ifStatement = self.compileIf()
                node.addChild(ifStatement)
            elif self.have(['keyword'], ['while']):
                whileStatement = self.compileWhile()
                node.addChild(whileStatement)
            elif self.have(['keyword'], ['do']):
                doStatement = self.compileDo()
                node.addChild(doStatement)
            elif self.have(['keyword'], ['return']):
                returnStatement = self.compileReturn()
                node.addChild(returnStatement)
            else:
                break
        return node
    
    
    def compileLet(self):
        """
        Generates a parse tree for a let statement
        @return a ParseTree that represents the statement
        """
        node = ParseTree('letStatement', None)

        kw1 = self.mustbe(['keyword'], ['let'])
        node.addChild(ParseTree(kw1.getType(), kw1.getValue()))

        id = self.mustbe(['identifier'], None)
        node.addChild(ParseTree(id.getType(), id.getValue()))

        if self.have(['symbol'], ['[']): 
            sym = self.mustbe(['symbol'], ['['])
            node.addChild(ParseTree(sym.getType(), sym.getValue()))

            expression = self.compileExpression()
            node.addChild(expression)

            sym = self.mustbe(['symbol'], [']'])
            node.addChild(ParseTree(sym.getType(), sym.getValue()))

        sym = self.mustbe(['symbol'], ['='])
        node.addChild(ParseTree(sym.getType(), sym.getValue()))

        expression = self.compileExpression()
        node.addChild(expression)

        sym = self.mustbe(['symbol'], [';'])
        node.addChild(ParseTree(sym.getType(), sym.getValue()))

        return node


    def compileIf(self):
        """
        Generates a parse tree for an if statement
        @return a ParseTree that represents the statement
        """
        node = ParseTree('ifStatement', None)

        kw = self.mustbe(['keyword'], ['if'])
        node.addChild(ParseTree(kw.getType(), kw.getValue()))

        sym = self.mustbe(['symbol'], ['('])
        node.addChild(ParseTree(sym.getType(), sym.getValue()))

        expression = self.compileExpression()
        node.addChild(expression)

        sym = self.mustbe(['symbol'], [')'])
        node.addChild(ParseTree(sym.getType(), sym.getValue()))

        sym = self.mustbe(['symbol'], ['{'])
        node.addChild(ParseTree(sym.getType(), sym.getValue()))

        statements = self.compileStatements()
        node.addChild(statements)

        sym = self.mustbe(['symbol'], ['}'])
        node.addChild(ParseTree(sym.getType(), sym.getValue()))

        if self.have(['keyword'], ['else']):
            kw = self.mustbe(['keyword'], ['else'])
            node.addChild(ParseTree(kw.getType(), kw.getValue()))

            sym = self.mustbe(['symbol'], ['{'])
            node.addChild(ParseTree(sym.getType(), sym.getValue()))

            statements = self.compileStatements()
            node.addChild(statements)

            sym = self.mustbe(['symbol'], ['}'])
            node.addChild(ParseTree(sym.getType(), sym.getValue()))

        return node

    
    def compileWhile(self):
        """
        Generates a parse tree for a while statement
        @return a ParseTree that represents the statement
        """

        node = ParseTree('whileStatement', None)

        kw = self.mustbe(['keyword'], ['while'])
        node.addChild(ParseTree(kw.getType(), kw.getValue()))

        sym = self.mustbe(['symbol'], ['('])
        node.addChild(ParseTree(sym.getType(), sym.getValue()))

        expression = self.compileExpression()
        node.addChild(expression)

        sym = self.mustbe(['symbol'], [')'])
        node.addChild(ParseTree(sym.getType(), sym.getValue()))

        sym = self.mustbe(['symbol'], ['{'])
        node.addChild(ParseTree(sym.getType(), sym.getValue()))

        statements = self.compileStatements()
        node.addChild(statements)

        sym = self.mustbe(['symbol'], ['}'])
        node.addChild(ParseTree(sym.getType(), sym.getValue()))

        return node


    def compileDo(self):
        """
        Generates a parse tree for a do statement
        @return a ParseTree that represents the statement
        """
        node = ParseTree('doStatement', None)

        kw = self.mustbe(['keyword'], ['do'])
        node.addChild(ParseTree(kw.getType(), kw.getValue()))

        expression = self.compileExpression()
        node.addChild(expression)

        sym = self.mustbe(['symbol'], [';'])
        node.addChild(ParseTree(sym.getType(), sym.getValue()))

        return node


    def compileReturn(self):
        """
        Generates a parse tree for a return statement
        @return a ParseTree that represents the statement
        """
        node = ParseTree('returnStatement', None)

        kw = self.mustbe(['keyword'], ['return'])
        node.addChild(ParseTree(kw.getType(), kw.getValue()))
        
        while not self.have(['symbol'], [';']) :
            expression = self.compileExpression()
            node.addChild(expression)

        sym = self.mustbe(['symbol'], [';'])
        node.addChild(ParseTree(sym.getType(), sym.getValue()))

        return node


    def compileExpression(self):
        """
        Generates a parse tree for an expression
        @return a ParseTree that represents the expression
        """

        node = ParseTree('expression', None)

        if self.have(['keyword'], ['skip']):
            skip = self.mustbe(['keyword'], ['skip']) 
            node.addChild(ParseTree(skip.getType(), skip.getValue()))
            return node
        node.addChild(self.compileTerm())

        while self.have(['symbol'],['+', '-', '*', '/', '&', '|', '<', '>', '=']):
            sym = self.mustbe(['symbol'], ['+', '-', '*', '/', '&', '|', '<', '>', '='])
            node.addChild(ParseTree(sym.getType(), sym.getValue()))
            node.addChild(self.compileTerm())
        return node


    def compileTerm(self):
        """
        Generates a parse tree for an expression term
        @return a ParseTree that represents the expression term
        """

        node = ParseTree('term', None)

        if self.have(['integerConstant', 'stringConstant'], None):
            tok = self.mustbe(['integerConstant', 'stringConstant'], None)
            node.addChild(ParseTree(tok.getType(), tok.getValue()))
        elif self.have(['keyword'], ['true','false','null','this']):
            tok = self.mustbe(['keyword'], ['true','false','null','this'])
            node.addChild(ParseTree(tok.getType(), tok.getValue()))
        elif self.have(['identifier'], None):
            id = self.mustbe(['identifier'], None)
            node.addChild(ParseTree(id.getType(), id.getValue()))
            if self.have(['symbol'], ['[']):
                sym = self.mustbe(['symbol'], ['['])
                node.addChild(ParseTree(sym.getType(), sym.getValue()))
                node.addChild(self.compileExpression())
                sym = self.mustbe(['symbol'], [']'])
                node.addChild(ParseTree(sym.getType(), sym.getValue()))

            elif self.have(['symbol'], ['(', '.']):

                if self.have(['symbol'], ['.']):
                    sym = self.mustbe(['symbol'], ['.'])
                    node.addChild(ParseTree(sym.getType(), sym.getValue()))
                    sub_tok = self.mustbe(['identifier'], None)
                    node.addChild(ParseTree(sub_tok.getType(), sub_tok.getValue()))

                sym = self.mustbe(['symbol'], ['('])
                node.addChild(ParseTree(sym.getType(), sym.getValue()))

                node.addChild(self.compileExpressionList())

                sym = self.mustbe(['symbol'], [')'])
                node.addChild(ParseTree(sym.getType(), sym.getValue()))
        elif self.have(['symbol'], ['(']):
            sym = self.mustbe(['symbol'], ['('])
            node.addChild(ParseTree(sym.getType(), sym.getValue()))

            node.addChild(self.compileExpression())

            sym = self.mustbe(['symbol'], [')'])
            node.addChild(ParseTree(sym.getType(), sym.getValue()))
        elif self.have(['symbol'], ['-','~']):
            sym = self.mustbe(['symbol'], ['-','~'])
            node.addChild(ParseTree(sym.getType(), sym.getValue()))
            node.addChild(self.compileTerm())
        return node


    def compileExpressionList(self):
        """
        Generates a parse tree for an expression list
        @return a ParseTree that represents the expression list
        """
        node = ParseTree('expressionList', None)

        if not self.have(['symbol'], [')']):
            node.addChild(self.compileExpression())
            while self.have(['symbol'], [',']):
                comma = self.mustbe(['symbol'], [','])
                node.addChild(ParseTree(comma.getType(), comma.getValue()))
                node.addChild(self.compileExpression())

        return node

    

if __name__ == "__main__":


    """ 
    Tokens for:
        class MyClass {
        
        }
    """
    tokens = []
    tokens.append(Token("keyword","class"))
    tokens.append(Token("identifier","MyClass"))
    tokens.append(Token("symbol","{"))
    tokens.append(Token("symbol","}"))

    parser = CompilerParser(tokens)
    try:
        result = parser.compileProgram()
        print(result)
    except ParseException:
        print("Error Parsing!")
