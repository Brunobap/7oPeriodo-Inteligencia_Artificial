
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
  arvore = {}
  for i = 1,12 do 
    table.insert(disponiveis, i)
  end
  
  
  mat = {
    {'.','','.','','.'},
    {'','X','','X',''},
    {'.','','.','','.'},
    {'','X','','X',''},
    {'.','','.','','.'}
  }
  
  -- Iniciar o jogo com a jogada da máquina
  -- Inicialmente, tirar uma posição random
  local aux = table.remove(disponiveis, math.random(1,12))
  jogadaPC(aux)
end
--

function love.mousepressed(x,y)
  -- Posições em blocos de 50
  local posX, posY = math.floor(x/50), math.floor(y/50)
  
  -- Verificação de jogadas erradas
  if ((x<50 or x>300) or (y<50 or y>300)) or mat[posY][posX] ~= '' then return end
  
  if (isPlyr) then
    mat[posY][posX] = 'Pl'
  else
    mat[posY][posX] = 'IA'    
  end
  
  checkClick(posX,posY)
  
  table.insert(arvore, Node.new(isPlyr, disponiveis))
  
  isPlyr = not isPlyr  
end
--

function checkClick(x,y)
  -- Bordas do tabuleiro, checar um quadrado
  if x == 1 or y == 1 or x == 5 or y == 5 then
    -- Borda esquerda
    if x == 1 then
      if mat[y][2] == 'X' and mat[y][3] ~= '' and mat[y-1][2] ~= '' and mat[y+1][2] ~= '' then marcou(2,y) end
      
    -- Borda superior
  elseif y == 1 then
      if mat[2][x] == 'X' and mat[3][x] ~= '' and mat[2][x+1] ~= '' and mat[2][x-1] ~= '' then marcou(x,2) end
      
      -- Borda direita
    elseif x == 5 then
      if mat[y][4] == 'X' and mat[y][3] ~= '' and mat[y-1][4] ~= '' and mat[y+1][4] ~= '' then marcou(4,y) end
      
    -- Borda inferior
    else
      if mat[4][x] == 'X' and mat[3][x] ~= '' and mat[4][x+1] ~= '' and mat[4][x-1] ~= '' then marcou(x,4) end
      
    end
  -- Interior do tabuleiro, checar dois quadrados
  else
    local temp = isPlyr
    -- Linha vertical do meio
    if x == 3 then
      if mat[y][2] == 'X' and mat[y][1] ~= '' and mat[y-1][2] ~= '' and mat[y+1][2] ~= '' then 
        marcou(2,y)
        isPlyr = not isPlyr
      end
      if mat[y][4] == 'X' and mat[y][5] ~= '' and mat[y-1][4] ~= '' and mat[y+1][4] ~= '' then
        marcou(4,y)
        isPlyr = not isPlyr
      end
      
    -- Linha horizontal do meio
    else
      if mat[2][x] == 'X' and mat[1][x] ~= '' and mat[2][x-1] ~= '' and mat[2][x+1] ~= '' then 
        marcou(x,2)
        isPlyr = not isPlyr
      end
      if mat[4][x] == 'X' and mat[5][x] ~= '' and mat[4][x-1] ~= '' and mat[4][x+1] ~= '' then
        marcou(x,4)
        isPlyr = not isPlyr
      end
    end
  end
end
--

function jogadaPC(pos)
  pos = (pos*2)-1
  local x,y = 55+50*(pos%5), 55+50*math.floor(pos/5)
  love.mousepressed(x,y)
end
--

function marcou(x,y)
  if isPlyr then mat[y][x] = 'Pl'
  else mat[y][x] = 'IA' end
  isPlyr = not isPlyr
end
--

function love.keypressed(k)
  if k == 'escape' then love.event.quit() end
end
--

function love.draw()
  -- Legenda ao lado
  LG.print('Pl = Jogador\nIA = Computador',350,50)
  
  -- Tabuleiro do jogo
  for i = 1,5 do
    for j = 1,5 do
      LG.rectangle('line',50*j,50*i,50,50)
      LG.print(mat[i][j],50*j,50*i)
    end
  end
end
