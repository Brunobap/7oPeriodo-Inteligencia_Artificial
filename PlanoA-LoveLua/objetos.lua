
Node = {}
Node.new = function(isPlyr, disponiveis)
  local self = self or {}
  
  self.isPlyr = isPlyr
  self.disponiveis = disponiveis
  self.filhos = {}
  
  return self
end
