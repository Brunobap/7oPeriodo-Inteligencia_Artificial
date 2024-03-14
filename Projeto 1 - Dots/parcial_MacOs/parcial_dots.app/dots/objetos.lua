
require('utilitarias')

Node = {}
Node.new = function(isPlyr, disponiveis, tabuleiro, usado)
  local self = self or {}
  
  self.disponiveis = disponiveis 
  
  usado = (usado*2)
  tabuleiro[usado] = "#"
  self.tabuleiro = tabuleiro

  self.isPlyr = isPlyr
  local x,y = usado%5, math.floor(usado/5)+1  
  if usado%5 == 0 then x = 5 end
  
  local finalState = checkClick(isPlyr, self.tabuleiro, x,y, usado)
  
  self.minmax = 0
  self.filhos = {}
  
  -- Se o nó já é um final da raíz, calcular o minmax
  if #self.disponiveis == 0 then
    if (self.tabuleiro[7] == 'PL') then self.minmax = self.minmax -1 else self.minmax = self.minmax +1 end
    if (self.tabuleiro[17] == 'PL') then self.minmax = self.minmax -1 else self.minmax = self.minmax +1 end
    if (self.tabuleiro[9] == 'PL') then self.minmax = self.minmax -1 else self.minmax = self.minmax +1 end
    if (self.tabuleiro[19] == 'PL') then self.minmax = self.minmax -1 else self.minmax = self.minmax +1 end
    
    if self.minmax ~= 0 then self.minmax = self.minmax/math.abs(self.minmax) end
    
  else
    -- Se não, fazer os nós dos filhos, ...
    for i,disp in ipairs(disponiveis) do 
      local auxTable = {}
      for j,disp1 in ipairs(disponiveis) do 
        if disp1 ~= disp then table.insert(auxTable, disp1) end
      end
      
      local novo = Node.new(finalState, auxTable, table.clone(self.tabuleiro), disp)
      table.insert(self.filhos, novo)
    end
    
    -- E com os nós dos filhos, pegar o minmax
      -- Se a vez é do jogador procurar o menor valor
    for i,filho in ipairs(self.filhos) do
      if (self.isPlyr and self.minmax > filho.minmax) or (not self.isPlyr and self.minmax < filho.minmax) then  self.minmax = filho.minmax end
    end
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
  table.insert(self, {isPlyr = false, disponiveis = table.clone(disponiveis), filhos = {}, tabuleiro = table.clone(tabuleiro)})
  
  for a,i in ipairs(disponiveis) do 
    if i == usado2 then table.remove(disponiveis, a) break end
  end  
  tabuleiro[usado2*2] = 'PL'
  table.insert(self[1].filhos, {isPlyr = true, disponiveis = table.clone(disponiveis), filhos = {}, tabuleiro = table.clone(tabuleiro)})
  
  local possibilidades, novo
  for i,disp in ipairs(disponiveis) do 
    possibilidades = {}
    for j,pos in ipairs(disponiveis) do
      if disp ~= pos then table.insert(possibilidades, pos) end
    end
    novo = Node.new(false, table.clone(possibilidades), table.clone(tabuleiro), disp)
    table.insert(self[1].filhos[1].filhos, novo)
  end
  --
  
  return self
end
