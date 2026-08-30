#pragma once

#ifndef CIV4_SYNC_LOG_H
#define CIV4_SYNC_LOG_H

//
// Per-turn record of the game state that has to match between multiplayer clients.
//
// When Civ4 goes out of sync it says so and nothing else. CvGame::calculateSyncChecksum
// folds the whole game into a single int, so a mismatch means "something, somewhere,
// differs" -- and it is worse than that: the checksum only covers ONE of its four state
// categories per turn slice,
//
//     switch (getTurnSlice() % 4)
//
// so a divergence in an unchecked category is not noticed until its slice comes round.
// By then the state that caused it has moved on and the report points nowhere near the
// cause.
//
// This writes a plain text line per player per turn covering ALL of those categories,
// every turn, on every client. Collect the file from two clients that went out of sync,
// diff them, and the first differing line names the turn, the player and the field.
//
// It deliberately does NOT touch calculateSyncChecksum or feed anything back into game
// state. Changing what the checksum covers would change the value every client computes,
// which is a way to CAUSE desyncs while trying to debug them. This only observes.
//
// Off unless SYNC_LOG is set in GlobalDefinesAlt.xml:
//
//     1  one summary line per player per turn -- cheap, safe to ask a player to enable
//     2  adds a line per unit -- large files, for when a divergence is already narrowed
//
// An ini/XML switch is right here, unlike the save format: this is a diagnostic a player
// needs to be able to turn on when asked to reproduce something, and it cannot corrupt
// anything if they leave it on.
//
namespace CvSyncLog
{
	// Cheap enough to call freely; the define is read once.
	bool isEnabled();

	// Call once per game turn, on every client. Safe to call when disabled.
	void logTurn();
}

#endif // CIV4_SYNC_LOG_H
