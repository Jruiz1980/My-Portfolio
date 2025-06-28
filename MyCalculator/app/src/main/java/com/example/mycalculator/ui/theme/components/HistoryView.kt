package com.example.mycalculator.ui.theme.components

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

/**
 * Composable function to display a list of calculation history entries and provided actions.
 * It uses a LazyColumn for efficient display of potentially long lists.
 *
 * @param history A list of strings, where each string represents a past calculation
 *                (e.g., "2 + 2 = 4").
 * @param modifier Modifier for this composable, allowing for custom styling and layout.
 * @param actions A composable slot for actions related to the history, like a reset button.
 */
@Composable
fun HistoryView(
    history: List<String>,
    modifier: Modifier = Modifier,
    actions: @Composable () -> Unit = {}
) {
    // Main Column to organize history and actions
    Column(
        modifier = modifier.fillMaxSize() // Occupies all space assigned by the parent (e.g., weight(0.2f))
    ) {
        if (history.isEmpty()) {
            // If history is empty, display "Empty" and actions below
            Column(
                modifier = Modifier
                    .weight(1f) // Occupies available space
                    .fillMaxWidth()
                    .padding(8.dp),
                horizontalAlignment = Alignment.CenterHorizontally,
                verticalArrangement = Arrangement.Center // Centers "Empty" text and the button
            ) {
                Text("Empty", fontSize = 14.sp)
                Box(modifier = Modifier.padding(top = 8.dp)) { // Space between "Empty" text and the button
                    actions() // Displays the Reset button
                }
            }
        } else {
            // If there's history, display the list and actions below
            // LazyColumn for the history, flexibly occupying available space
            LazyColumn(
                modifier = Modifier
                    .weight(1f) // This is CRUCIAL so it doesn't push actions out
                    .fillMaxWidth()
                    .padding(horizontal = 8.dp, vertical = 4.dp), // Adjust padding if necessary
                reverseLayout = true
            ) {
                items(history) { historyEntry ->
                    Text(
                        text = historyEntry,
                        fontSize = 16.sp,
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(vertical = 2.dp),
                        textAlign = TextAlign.End // Aligns history text to the right (common in calculators)
                    )
                }
            }
            // Box for actions (Reset button), always visible below the history
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(vertical = 4.dp), // Padding for the button
                contentAlignment = Alignment.Center // Centers the button horizontally
            ) {
                actions() // Displays the Reset button
            }
        }
    }
}