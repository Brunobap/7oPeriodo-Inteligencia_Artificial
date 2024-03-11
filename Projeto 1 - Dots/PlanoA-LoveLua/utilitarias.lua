
function checkClick(isPlyr,mat,x,y,abs)
  -- Bordas do tabuleiro, checar um quadrado
  if x == 1 or y == 1 or x == 5 or y == 5 then
    -- Borda esquerda
    if x == 1 then
      if mat[abs+1] == 'X' and (mat[abs-4] ~= '' and mat[abs+6] ~= '' and mat[abs+2] ~= '') then
        marcou(isPlyr,mat,abs+1)
        return isPlyr
      end
      
    -- Borda superior
  elseif y == 1 then
      if mat[abs+5] == 'X' and (mat[abs+4] ~= '' and mat[abs+10] ~= '' and mat[abs+6] ~= '') then
        marcou(isPlyr,mat,abs+5)
        return isPlyr
      end
      
      -- Borda direita
    elseif x == 5 then
      if mat[abs-1] == 'X' and (mat[abs-6] ~= '' and mat[abs+5] ~= '' and mat[abs-2] ~= '') then
        marcou(isPlyr,mat,abs-1)
        return isPlyr
      end
      
    -- Borda inferior
    else
      if mat[abs-5] == 'X' and (mat[abs-6] ~= '' and mat[abs-4] ~= '' and mat[abs-10] ~= '') then
        marcou(isPlyr,mat,abs-5)
        return isPlyr 
      end
    end
  -- Interior do tabuleiro, checar dois quadrados
  else
    local flag = false
    -- Linha vertical do meio
    if x == 3 then
      if mat[abs-1] == 'X' and mat[abs-6] ~= '' and mat[abs+4] ~= '' and mat[abs-2] ~= '' then 
        flag = true
        marcou(isPlyr,mat,abs-1)
      end
      if mat[abs+1] == 'X' and mat[abs-4] ~= '' and mat[abs+6] ~= '' and mat[abs+2] ~= '' then
        flag = true
        marcou(isPlyr,mat,abs+1)
      end
      
    -- Linha horizontal do meio
    else
      if mat[abs-5] == 'X' and mat[abs-10] ~= '' and mat[abs-4] ~= '' and mat[abs-6] ~= '' then 
        marcou(isPlyr,mat,abs-5)
        flag = true
      end
      if mat[abs+5] == 'X' and mat[abs+10] ~= '' and mat[abs+4] ~= '' and mat[abs+6] ~= '' then
        marcou(isPlyr,mat,abs+5)
        flag = true
      end
    end
    if flag then return isPlyr end
  end
  return not isPlyr
end
--
function jogadaPC(pos)
  pos = (pos*2)-1
  local x,y = 75+50*(pos%5), 75+50*math.floor(pos/5)
  love.mousepressed(x,y)
end
--
function marcou(isPlyr,mat,pos)
  if isPlyr then mat[pos] = 'PL'
  else mat[pos] = 'IA' end
end
