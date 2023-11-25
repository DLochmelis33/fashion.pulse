package cub.dlhf.fashionpulse

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.IntrinsicSize
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.width
import androidx.compose.material3.Button
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp

@Composable
fun ImagePicker(
    takePhotoCallback: () -> Unit,
    pickImageCallback: () -> Unit,
) {
    Row(
        horizontalArrangement = Arrangement.SpaceEvenly,
        modifier = Modifier
            .height(IntrinsicSize.Max)
    ) {
        Button(
            onClick = { takePhotoCallback() }, modifier = Modifier
                .fillMaxSize()
                .weight(1f)
        ) {
            Text(text = "Take a photo", textAlign = TextAlign.Center)
        }
        Spacer(modifier = Modifier.width(3.dp))
        Button(
            onClick = { pickImageCallback() }, modifier = Modifier
                .fillMaxSize()
                .weight(1f)
        ) {
            Text(text = "Pick from gallery", textAlign = TextAlign.Center)
        }
    }
}
