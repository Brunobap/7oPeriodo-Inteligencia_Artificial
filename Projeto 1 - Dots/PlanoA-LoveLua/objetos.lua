
local contagem

Node = {}
Node.new = function(isPlyr, disponiveis)
  local self = self or {}
  
  self.isPlyr = not isPlyr
  self.disponiveis = disponiveis
  
  self.filhos = {}
  local novo, auxTable
  
  -- Para toda jogada restante
  for i,disp in ipairs(disponiveis) do 
    -- Montar a tabela de disponíveis
    auxTable = {}
    for j,disp1 in ipairs(disponiveis) do 
      if disp1 ~= disp then table.insert(auxTable, disp1) end
    end
    
    --print(table.maxn(disponiveis))
    
    -- Montar o nó com as possibilidades daquela jogada
    -- To do: checar de quem é a próxima jogada
    novo = Node.new(isPlyr, auxTable)
    table.insert(self.filhos, novo)
  end
  --
  if table.maxn(self.disponiveis) == 0 then
    contagem = contagem +1
    if contagem % 1e4 == 0 then print(contagem) end
  end
  
  return self
end
--

Arvore = {}
Arvore.new = function(usado1, usado2)
  local self = self or {}
  
  contagem = 0
  
  local disponiveis = {}
  for i = 1,12 do 
    if i ~= usado1 then table.insert(disponiveis, i) end
  end  
  table.insert(self, {isPlyr = true, disponiveis = disponiveis, filhos = {}})
  
  for a,i in ipairs(disponiveis) do 
    if i == usado2 then table.remove(disponiveis, i) break end
  end  
  table.insert(self[1].filhos, {isPlyr = false, disponiveis = disponiveis, filhos = {}})
  
  local possibilidades, novo
  for i,disp in ipairs(disponiveis) do 
    possibilidades = {}
    for j,pos in ipairs(disponiveis) do
      if disp ~= pos then table.insert(possibilidades, pos) end
    end
    novo = Node.new(false, possibilidades)
    table.insert(self[1].filhos[1].filhos, novo)
  end
  --
  
  return self
end
--