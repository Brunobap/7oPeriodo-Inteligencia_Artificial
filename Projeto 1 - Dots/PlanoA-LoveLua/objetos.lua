
local contagem

Node = {}
Node.new = function(isPlyr, disponiveis, tabuleiro, usado)
  local self = self or {}
  
  self.isPlyr = not isPlyr
  self.disponiveis = disponiveis
  self.tabuleiro = tabuleiro
  
  usado = (usado*2)-1
  if (isPlyr) then self.tabuleiro[usado] = 'PL'
  else self.tabuleiro[usado] = 'IA' end
  local x,y = (usado%5), math.floor(usado/5)
  checkClick(self.tabuleiro,x,y,usado)
  
  self.minmax = nil -- ???
  
  self.filhos = {}
  local novo, auxTable
  
  -- Para toda jogada restante
  for i,disp in ipairs(disponiveis) do 
    -- Montar a tabela de disponíveis
    auxTable = {}
    for j,disp1 in ipairs(disponiveis) do 
      if disp1 ~= disp then table.insert(auxTable, disp1) end
    end
    
    -- Montar o nó com as possibilidades daquela jogada
    -- To do: checar de quem é a próxima jogada
    novo = Node.new(isPlyr, auxTable)
    table.insert(self.filhos, novo)
  end
  --
  if table.maxn(self.disponiveis) == 0 then
    
  end
  
  return self
end
--
Arvore = {}
Arvore.new = function(usado1, usado2, tabuleiro)
  local self = self or {}
  
  contagem = 0
  
  local disponiveis = {}
  for i = 1,12 do 
    if i ~= usado1 then table.insert(disponiveis, i) end
  end  
  tabuleiro[usado1*2] = 'IA'
  table.insert(self, {isPlyr = false, disponiveis = disponiveis, filhos = {}, tabuleiro = tabuleiro})
  
  
  for a,i in ipairs(disponiveis) do 
    if i == usado2 then table.remove(disponiveis, i) break end
  end  
  tabuleiro[usado2*2] = 'PL'
  table.insert(self[1].filhos, {isPlyr = true, disponiveis = disponiveis, filhos = {}, tabuleiro = tabuleiro})
  
  local possibilidades, novo
  for i,disp in ipairs(disponiveis) do 
    possibilidades = {}
    for j,pos in ipairs(disponiveis) do
      if disp ~= pos then table.insert(possibilidades, pos) end
    end
    novo = Node.new(false, possibilidades, tabuleiro)
    table.insert(self[1].filhos[1].filhos, novo)
  end
  --
  
  return self
end
--