
-- Apelidos
local LG = love.graphics

-- Matriz principal
local mat

-- Flag da vez do jogador
local isPlyr

-- Aviso de jogada errada
local aviso

function love.load()
  -- Setando a parte gráfica da tela
  LG.setBackgroundColor(1,1,1,1)
  LG.setColor(0,0,0,1)
  LG.setNewFont(40)
  
  -- Iniciando as variáveis
  isPlyr = true
  aviso = ''
  mat = {
    {'.','--','.','--','.'},
    {'|','','|','','|'},
    {'.','--','.','--','.'},
    {'|','','|','','|'},
    {'.','--','.','--','.'}
  }
end
--

function love.mousepressed(x,y)
  if (isPlyr) then
    
  else
  
  end
end
--

function love.keypressed(k)
  if k == 'escape' then love.event.quit() end
end
--

function love.draw()
  -- Legenda ao lado
  LG.print('Jg = Jogador\nIA = Computador',350,50)
  
  -- Tabuleiro do jogo
  for i = 1,5 do
    for j = 1,5 do
      LG.rectangle('line',50*j,50*i,50,50)
      LG.print(mat[i][j],50*j,50*i)
    end
  end
  --
  -- Aviso (caso haja um clique errado)
  LG.print(aviso, 50, 350)
end
