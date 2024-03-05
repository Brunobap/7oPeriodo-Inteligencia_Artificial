
require('objetos')

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

  -- Iniciar o jogo com a jogada da máquina
  -- Inicialmente, tirar uma posição random
  local aux1 = table.remove(disponiveis, math.random(1,12))
  jogadaPC(aux1)
  
  local aux2 = table.remove(disponiveis, math.random(1,11))
  jogadaPC(aux2)
  
  arvore = Arvore.new(aux1, aux2)
  
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
  
  checkClick(posX,posY,posAbs)
  
  isPlyr = not isPlyr  
end
--
function checkClick(x,y,abs)
  -- Bordas do tabuleiro, checar um quadrado
  if x == 1 or y == 1 or x == 5 or y == 5 then
    -- Borda esquerda
    if x == 1 then
      if mat[abs+1] == 'X' and (mat[abs-4] ~= '' and mat[abs+6] ~= '' and mat[abs+2] ~= '') then marcou(abs+1) end
      
    -- Borda superior
  elseif y == 1 then
      if mat[abs+5] == 'X' and (mat[abs+4] ~= '' and mat[abs+10] ~= '' and mat[abs+6] ~= '') then marcou(abs+5) end
      
      -- Borda direita
    elseif x == 5 then
      if mat[abs-1] == 'X' and (mat[abs-6] ~= '' and mat[abs+5] ~= '' and mat[abs-2] ~= '') then marcou(abs-1) end
      
    -- Borda inferior
    else
      if mat[abs-5] == 'X' and (mat[abs-6] ~= '' and mat[abs-4] ~= '' and mat[abs-10] ~= '') then marcou(abs-5) end
      
    end
  -- Interior do tabuleiro, checar dois quadrados
  else
    local flag = false
    -- Linha vertical do meio
    if x == 3 then
      if mat[abs-1] == 'X' and mat[abs-6] ~= '' and mat[abs+4] ~= '' and mat[abs-2] ~= '' then 
        marcou(abs-1)
        isPlyr = not isPlyr
        flag = true
      end
      if mat[abs+1] == 'X' and mat[abs+4] ~= '' and mat[abs+6] ~= '' and mat[abs+2] ~= '' then
        if flag then isPlyr = not temp end
        marcou(abs+1)
      end
      
    -- Linha horizontal do meio
    else
      if mat[abs-5] == 'X' and mat[abs-10] ~= '' and mat[abs-4] ~= '' and mat[abs-6] ~= '' then 
        marcou(abs-5)
        isPlyr = not temp
      end
      if mat[abs+5] == 'X' and mat[abs+10] ~= '' and mat[abs+4] ~= '' and mat[abs+6] ~= '' then
        marcou(abs+5)
        isPlyr = not temp
      end
    end
  end
end
--
function jogadaPC(pos)
  pos = (pos*2)-1
  local x,y = 75+50*(pos%5), 75+50*math.floor(pos/5)
  love.mousepressed(x,y)
end
--
function marcou(pos)
  if isPlyr then mat[pos] = 'PL'
  else mat[pos] = 'IA' end
  isPlyr = not isPlyr
end
--
function love.keypressed(k)
  if k == 'escape' then love.event.quit() end
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
