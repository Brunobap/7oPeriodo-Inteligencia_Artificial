require('objetos')
require('utilitarias')

-- Apelido
local LG = love.graphics
-- Matriz principal
local mat
-- Flag da vez do jogador
local isPlyr
-- Número de jogadas (para acompanhar o nível da árvore)
local jogadas
-- Ponteiro para a última jogada feita 
local noAtual

function love.load()
  -- Seed de randoms  
  math.randomseed(os.time())
  
  -- Setando a parte gráfica da tela
  LG.setBackgroundColor(1,1,1,1)
  LG.setColor(0,0,0,1)
  LG.setNewFont(35)
  
  -- Iniciando as variáveis
  isPlyr = false
  jogadas = 0  
  
  local disponiveis = {}  
  for i = 1,12 do table.insert(disponiveis, i) end  
  
  mat = {
    '.',  '',   '.',  '',   '.',
    
    '',   'X',  '',   'X',  '',
    
    '.',  '',   '.',  '',   '.',
    
    '',   'X',  '',   'X',  '',
    
    '.',  '',   '.',  '',   '.'
  }
 
  -- Iniciar com jogadas random
  local aux1 = table.remove(disponiveis, math.random(1,12))  
  local aux2 = table.remove(disponiveis, math.random(1,11))
  
  jogadaPC(aux1)
  jogadaPC(aux2)
  
  noAtual = Arvore.new(aux1, aux2)
  
  jogadaPC(noAtual.filhos[1].usado)
end
--
function love.mousepressed(x,y)
  -- Posições em blocos de 50
  local posX, posY = math.floor(x/50), math.floor(y/50)
  
  -- Posição no vetor de 25 posições
  local posAbs = (posX + 5*(posY+1))-10
  
  -- Verificação de jogadas erradas
  if ((x<50 or x>300) or (y<50 or y>300)) or mat[posAbs] ~= '' then return end
  
  if isPlyr then mat[posAbs] = 'PL' else mat[posAbs] = 'IA' end
  
  isPlyr = checkClick(isPlyr, mat, posX,posY, posAbs)
 
  jogadas = jogadas +1 
  
  -- As 2 primeiras jogadas são random, as próximas vão cortando a árvore
  if 2 < jogadas and jogadas < 12 then
    posAbs = posAbs / 2
    local temp
    for i,filho in ipairs(noAtual.filhos) do   
      if filho.usado == posAbs then temp = filho break end
    end
    
    noAtual = temp
    
    if not isPlyr then 
      print(noAtual.minmax)
      for i,filho in ipairs(noAtual.filhos) do
        if filho.minmax == noAtual.minmax then jogadaPC(filho.usado) break end
      end      
    end
  end
end
--
function love.keypressed(k)
  if k == 'r' then
    noAtual = nil
    love.load()
  else love.event.quit() end
end
--
function love.draw()
  -- Legenda ao lado
  LG.print('PL = Jogador\nIA = Computador',350,50)
  LG.print('Jogadas restantes: '..(12-jogadas),50,350)
  
  -- Tabuleiro do jogo
  local x,y
  for i,char in ipairs(mat) do
    x,y = 50+50*((i-1)%5), 50+50*math.floor((i-1)/5)
    LG.rectangle('line',x,y,50,50)
    LG.printf(char,x,y,50,'center')
  end
end
