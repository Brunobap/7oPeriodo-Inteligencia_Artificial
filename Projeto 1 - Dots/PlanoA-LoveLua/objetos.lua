
local contagem

Node = {}
Node.new = function(isPlyr, disponiveis)
  local self = self or {}
  
  self.isPlyr = isPlyr
  self.disponiveis = disponiveis
  
  self.filhos = {}
  local novo, auxTable
  for i,disp in ipairs(disponiveis) do 
    auxTable = {}
    for j,disp1 in ipairs(disponiveis) do 
      if disp1 ~= disp then table.insert(auxTable, disp1) end
    end
    table.remove(auxTable, i)
    novo = Node.new(isPlyr, auxTable)
    table.insert(self.filhos, novo)
    contagem = contagem +1
    print(contagem)
  end
  --
  
  return self
end
--

Arvore = {}
Arvore.new = function()
  local self = self or {}
  
  contagem = 0
  
  local possibilidades, novo
  for i = 1,12 do 
    possibilidades = {}
    for j = 1,12 do
      if i ~= j then table.insert(possibilidades, j) end
    end
    novo = Node.new(true, possibilidades)
    table.insert(self, novo)
  end
  --
  
  return self
end
--