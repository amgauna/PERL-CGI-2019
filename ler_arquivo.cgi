#!/usr/bin/env tclsh
#Script ler_arquivo.tcl

  set nome_canal [ open arquivos.txt r ]

  while { ! [ eof $nome_canal ] } {
         set linha [ gets $nome_canal ]
         puts "Esta linha contém: $linha"
  }
