<?php
    $results = fopen('./resultslogs.log', a);
    for($i = 1; $i < 13; $i++)
    {
        for($j = 0; $j < 3; $j++)
        {
            $file = './log'.$i.'image'.(($i == 1)? "" : 's').(($j < 1)? 'EigenFace' : (($j < 2)? 'FisherFace' : 'LBPH'));
            if(file_exists($file))
            {
                $ofile = fopen($file, 'r');
                $ajout = array();
                $reco = array();
                while(($buffer = fgets($ofile)) !== false)
                {
                    if(preg_match("#^L'ajout des images dans la bdd a pris :#", $buffer))
                    {
                        $ajout[] = floatval(preg_replace("#[^0-9.]#", "", $buffer));
                    }
                    else if(preg_match("#^La reconnaissance a pris :#", $buffer))
                    {
                        $reco[] = floatval(preg_replace("#[^0-9.]#", "", $buffer));
                    }
                }
                $moyAjout = (count($ajout) == 0)? 0 : (array_sum($ajout) / count($ajout));
                $moyReco= (count($reco) == 0)? 0 : (array_sum($reco) / count($reco));
                
                $res = $file . " : L'ajout des images dans la bdd a pris : " . $moyAjout . "\n" . $file . " : La reconnaissance a pris : " . $moyReco . "\n";
                echo($res);
                
                fputs($results, $res);
                fclose($ofile);
                
            }
        }
    }
    fclose($results);
?>
