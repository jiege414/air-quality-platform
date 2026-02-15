package com.cugb.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.cugb.entity.AirQualityRealtime;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;

import java.util.List;

@Mapper
public interface AirQualityRealtimeMapper extends BaseMapper<AirQualityRealtime> {
    
    @Select("SELECT * FROM air_quality_realtime ORDER BY aqi DESC LIMIT #{limit}")
    List<AirQualityRealtime> selectTop10ByAqiDesc(Integer limit);
    
    @Select("SELECT * FROM air_quality_realtime ORDER BY aqi ASC LIMIT #{limit}")
    List<AirQualityRealtime> selectTop10ByAqiAsc(Integer limit);
}
