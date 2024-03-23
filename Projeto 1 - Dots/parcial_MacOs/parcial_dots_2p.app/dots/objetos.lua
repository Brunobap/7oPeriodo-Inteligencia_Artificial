require('utilitarias')

Node = {}
Node.new = function(isPlyr, disponiveis, tabuleiro, usado)
  local self = {}
  
  self.usado = usado
  self.isPlyr = isPlyr
  self.filhos = {}
  
  usado = (usado*2)
  tabuleiro[usado] = "#"
  local x,y = usado%5, math.floor(usado/5)+1  
  if usado%5 == 0 then x = 5 end
  local finalState = checkClick(isPlyr, tabuleiro, x,y, usado)
  
  -- Se o nó já é um final da raíz, calcular o minmax
  if #disponiveis == 0 then
    self.minmax = 0
    if (tabuleiro[7] == 'PL') then self.minmax = self.minmax -1 else self.minmax = self.minmax +1 end
    if (tabuleiro[9] == 'PL') then self.minmax = self.minmax -1 else self.minmax = self.minmax +1 end
    if (tabuleiro[17] == 'PL') then self.minmax = self.minmax -1 else self.minmax = self.minmax +1 end
    if (tabuleiro[19] == 'PL') then self.minmax = self.minmax -1 else self.minmax = self.minmax +1 end
    
  else
    if self.isPlyr then self.minmax = 10 else self.minmax = -10 end
    -- Se não, fazer os nós dos filhos, ...
    for i,disp in ipairs(disponiveis) do 
      local auxTable = {}
      for j,disp1 in ipairs(disponiveis) do 
        if disp1 ~= disp then table.insert(auxTable, disp1) end
      end
      
      local novo = Node.new(finalState, auxTable, table.clone(tabuleiro), disp)
      if (self.isPlyr and self.minmax > novo.minmax) or (not self.isPlyr and self.minmax < novo.minmax) then self.minmax = novo.minmax end
      table.insert(self.filhos, novo)      
    end
    
--    if not self.isPlyr then
--      for i,filho in ipairs(self.filhos) do
--        if filho.minmax ~= self.minmax then table.remove(self.filhos, i) end
--      end
--      self.filhos = {self.filhos[1]}
--    end
  end
  
  return self
end
--
Arvore = {}
Arvore.new = function(usado1, usado2)
  local self = self or {}
  
  local tabuleiro = {
    '.',  '',   '.',  '',   '.',
    
    '',   'X',  '',   'X',  '',
    
    '.',  '',   '.',  '',   '.',
    
    '',   'X',  '',   'X',  '',
    
    '.',  '',   '.',  '',   '.'
  }
  
  local disponiveis = {}
  
  for i = 1,12 do if i ~= usado1 then table.insert(disponiveis, i) end end  
  tabuleiro[usado1*2] = 'IA'
  
  for a,i in ipairs(disponiveis) do 
    if i == usado2 then table.remove(disponiveis, a) break end
  end  
  tabuleiro[usado2*2] = 'PL'
  
  local atual = {
    isPlyr = true,
    filhos = {}, 
    minmax = 10
  }
  
  local possibilidades, novo
  for i,disp in ipairs(disponiveis) do 
    possibilidades = {}
    for j,pos in ipairs(disponiveis) do
      if disp ~= pos then table.insert(possibilidades, pos) end
    end
    novo = Node.new(false, possibilidades, table.clone(tabuleiro), disp)
    print(novo.usado)
    if atual.minmax < novo.minmax then atual.minmax = novo.minmax end
    table.insert(atual.filhos, novo)         
  end
  return atual
end
