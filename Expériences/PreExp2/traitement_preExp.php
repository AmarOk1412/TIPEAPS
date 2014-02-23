<?php
/*
 

_/\/\/\/\/\/\__/\/\/\/\__/\/\/\/\/\____/\/\/\/\/\/\______/\/\______/\/\/\/\/\______/\/\/\/\/\_
_____/\/\________/\/\____/\/\____/\/\__/\______________/\/\/\/\____/\/\____/\/\__/\/\_________
_____/\/\________/\/\____/\/\/\/\/\____/\/\/\/\/\____/\/\____/\/\__/\/\/\/\/\______/\/\/\/\___
_____/\/\________/\/\____/\/\__________/\/\__________/\/\/\/\/\/\__/\/\__________________/\/\_
_____/\/\______/\/\/\/\__/\/\__________/\/\/\/\/\/\__/\/\____/\/\__/\/\__________/\/\/\/\/\___
______________________________________________________________________________________________

 
 
 */

    $results = fopen('./results_recognize.log', a);

    function recognize($name)
    {
        $file = './reconnaissance'.$name;
        if(file_exists($file))
        {
            $ofile = fopen($file, 'r');
            $eigen = 0;
            $fisher = 0;
            $LBPH = 0;
            $nbeigen = 0;
            $nbfisher = 0;
            $nbLBPH = 0;
            while(($buffer = fgets($ofile)) !== false)
            {
                if(preg_match("#Eigenface#i", $buffer))
                {
                    $eigen += (preg_match("#".$name."#i", $buffer))? 1 : 0;
                    $nbeigen++;
                }
                else if(preg_match("#Fisherface#i", $buffer))
                {
                    $fisher += (preg_match("#".$name."#i", $buffer))? 1 : 0;
                    $nbfisher++;
                }
                else if(preg_match("#LBPH#i", $buffer))
                {
                    $LBPH += (preg_match("#".$name."#i", $buffer))? 1 : 0;
                    $nbLBPH++;
                }
            }
            return array(
                'eigenface' => ($nbeigen == 0)? 0 : (100 * $eigen / $nbeigen),
                'fisherface' => ($nbfisher == 0)? 0 : (100 * $fisher / $nbfisher),
                'LBPH' => ($nbLBPH == 0)? 0 : (100 * $LBPH / $nbLBPH));
        }
        else
            return $name . ' : Erreur';
    }

    $resA = recognize('Amaury');
    $resP = recognize('PHenri');
    $resS = recognize('Sebastien');

    fputs($results, 'Amaury : Eigenface = '.$resA['eigenface'].'% / fisherface = '.$resA['fisherface'].'% / LBPH = '.$resA['LBPH'].'%');
    fputs($results, 'Phenri : Eigenface = '.$resP['eigenface'].'% / fisherface = '.$resP['fisherface'].'% / LBPH = '.$resP['LBPH'].'%');
    fputs($results, 'Seb : Eigenface = '.$resS['eigenface'].'% / fisherface = '.$resS['fisherface'].'% / LBPH = '.$resS['LBPH'].'%');

    fclose($results);
?>