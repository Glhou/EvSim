# Energy Generator

This project is liked with the EvClient. It creates fake energy and make an auction.

## How does it works

The server will create fake energy when ideling for a certain time.

After that EvClient will contact the server to know about if they have energy and their price.

Then EvClient will accept to bid on the energy and an auction is launched.

Based on different criteria A EvClient will win the auction, the server will make the choice depending on the informations it has.

The server will ask the winner if he takes the energy, if so it will notify other that they loose, if it don't it will ask for the next EvClient.

Then for a certain time the energy will be delivered so the server will iddle.

## Goal

We don't want car without energy, so the objective is to have an average amount of energy always above 50%

## How is calculated the score

score = ( 5/ distance (km) + 100/energy (%) ) / nbGenInRng

## Issues and how the server should handle

1. If one EvClient only has one Energy Generator in it's range and can only get it's energy from it, it should win
2. If two client have the same score ask both of them, if the two replied yes pick one randomly (janken)
3. If in case 1 but there is an other client with very low energy 10% or less, this other client should get the energy
