import torch
import torch.nn as nn
import torch.nn.functional as F


class ChunkData(nn.Module):

    def __init__(self, chunk_size, target):
        super(ChunkData, self).__init__()

        self.chunk_size = chunk_size
        
        self.target = target
    
    def forward(self, dt):
        with torch.no_grad():

            time, freq = dt['mixed_mag'].shape

            device = dt['mixed_mag'].device

            dt['x'] = torch.zeros((time - self.chunk_size, self.chunk_size, freq), device= device)

            dt['y'] = torch.zeros((time - self.chunk_size, freq), device= device)

            for i in range(time - self.chunk_size):
                
                dt['x'][i, :, :] = dt['mixed_mag'][i : i + self.chunk_size, :]

                dt['y'][i, :] = dt[self.target][i + self.chunk_size, :]#predict mask

            
            dt['x'] = dt['x'].permute(0, 2, 1)

        return dt

    

class ChunkDatav2(nn.Module):

    def __init__(self, chunk_size, target):
        super(ChunkDatav2, self).__init__()

        self.chunk_size = chunk_size
        
        self.target = target
    
    def forward(self, dt):
        with torch.no_grad():

            time, freq = dt['mixed_mag'].shape

            device = dt['mixed_mag'].device

            chunks = time // self.chunk_size + 1
            
            dt['mixed_mag'] = F.pad(dt['mixed_mag'], (0, 0, 0, self.chunk_size - time % self.chunk_size))

            dt[self.target] = F.pad(dt[self.target], (0, 0, 0, self.chunk_size - time % self.chunk_size))

            dt['x'] = torch.zeros((chunks, self.chunk_size, freq), device= device)

            dt['y'] = torch.zeros((chunks, self.chunk_size, freq), device= device)

            for i in range(chunks):
                
                dt['x'][i] = dt['mixed_mag'][i * self.chunk_size : (i + 1) * self.chunk_size]
                
                dt['y'][i] = dt[self.target][i * self.chunk_size : (i + 1) * self.chunk_size] 
            
            dt['x'] = dt['x'].permute(0, 2, 1)

        return dt

class ChunkDatav3(nn.Module):

    def __init__(self, chunk_size, target):
        super(ChunkDatav3, self).__init__()

        self.chunk_size = chunk_size
        
        self.target = target
    
    def forward(self, dt):
        with torch.no_grad():

            time, freq = dt['mixed_mag'].shape

            device = dt['mixed_mag'].device

            chunks = time // self.chunk_size + 1

            dt['mixed_mag'] = F.pad(dt['mixed_mag'], (0, 0, 0, self.chunk_size - time % self.chunk_size))

            dt[self.target] = F.pad(dt[self.target], (0, 0, 0, self.chunk_size - time % self.chunk_size))

            dt['x'] = torch.zeros((chunks, self.chunk_size, freq), device= device)

            dt['y'] = torch.zeros((chunks, self.chunk_size, freq - 1), device= device)

            for i in range(chunks):
                
                dt['x'][i] = dt['mixed_mag'][i * self.chunk_size : (i + 1) * self.chunk_size, ]
                
                dt['y'][i] = dt[self.target][i * self.chunk_size : (i + 1) * self.chunk_size, : 256] 
            
            dt['x'] = dt['x'].permute(0, 2, 1)

        return dt
