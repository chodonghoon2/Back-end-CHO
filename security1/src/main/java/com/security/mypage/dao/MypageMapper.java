package com.security.mypage.dao;

import java.util.List;

import org.apache.ibatis.annotations.Mapper;

import com.security.mypage.dto.MypageAccountDto;
import com.security.mypage.dto.MypageGameRoomDto;
import com.security.mypage.dto.MypageWorkAccuracyDto;
import com.security.mypage.dto.MypageWorkBigThreeDto;

@Mapper
public interface MypageMapper {
	
	//자신의 개인 프로필
	public MypageAccountDto findByUsername(String username);
	
	//게임 기록
	public List<MypageGameRoomDto> findAllByNo(int accountNo);
	
	//운동별 정확도 증가 추이
	public List<MypageWorkAccuracyDto> findAccuracyAllByNo(int accountNo);
	//3대 운동 증가 추이(횟수?)
	public List<MypageWorkBigThreeDto> findBigThreeAllByNo(int accountNo);
}