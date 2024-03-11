
require('objetos')
require('utilitarias')

-- Apelidos
local LG = love.graphics

-- Matriz principal
local mat

-- Vetor de disponíveis
local disponiveis

-- Árvore de possibilidades
local arvore

-- Flag da vez do jogador
local isPlyr

-- Número de jogadas (para acompanhar o nível da árvore)
local jogadas

function love.load()
  -- Seed de randoms  
  math.randomseed(os.time())
  
  -- Setando a parte gráfica da tela
  LG.setBackgroundColor(1,1,1,1)
  LG.setColor(0,0,0,1)
  LG.setNewFont(40)
  
  -- Iniciando as variáveis
  isPlyr = false
  
  disponiveis = {}
  for i = 1,12 do 
    table.insert(disponiveis, i)
  end    
  
  -- Vetor para a representação na tela
  mat = {
    '.','','.','','.',
    '','X','','X','',
    '.','','.','','.',
    '','X','','X','',
    '.','','.','','.'
  }

  -- Iniciar com jogadas random
  local aux1 = table.remove(disponiveis, math.random(1,12))
  jogadaPC(aux1)
  
  local aux2 = table.remove(disponiveis, math.random(1,11))
  jogadaPC(aux2)
  
  --arvore = Arvore.new(aux1, aux2)
  
  -- Começa o jogo
  jogadas = 2
end
--
function love.mousepressed(x,y)
  -- Posições em blocos de 50
  local posX, posY = math.floor(x/50), math.floor(y/50)
  
  local posAbs = (posX + 5*(posY+1))-10
  
  -- Verificação de jogadas erradas
  if ((x<50 or x>300) or (y<50 or y>300)) or mat[posAbs] ~= '' then return end  
  
  if (isPlyr) then mat[posAbs] = 'PL'
  else mat[posAbs] = 'IA' end
  
  isPlyr = checkClick(isPlyr,mat,posX,posY,posAbs)
end
--
function love.keypressed(k)
  if k == 'r' then love.load()
  else love.event.quit() end
end
--
function love.draw()
  -- Legenda ao lado
  LG.print('PL = Jogador\nIA = Computador',350,50)
  
  -- Tabuleiro do jogo
  local x,y
  for i,char in ipairs(mat) do
    x,y = 50+50*((i-1)%5), 50+50*math.floor((i-1)/5)
    LG.rectangle('line',x,y,50,50)
    LG.print(char,x,y)
  end
end
